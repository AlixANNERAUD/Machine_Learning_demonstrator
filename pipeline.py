import csv
import io
import os
import threading
from queue import Queue

import numpy as np
import pydub
import requests
import torch
import torchaudio.transforms as T
from datasets import Audio, Dataset
from npy_append_array import NpyAppendArray
from torch import nn
from transformers import AutoModel, Wav2Vec2FeatureExtractor

cuda = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
print(f"Using device: {cuda}")

n_threads = 2
queue_size = 20

csv_file_path = "tracks.csv"
audio_folder = "audio_330"
ids_file_path = "processed_ids_330.txt"
embedding_file = "embeddings_330.npy"
embedding_id_file = f"id_{embedding_file}"
sampling_rate = 44100

# Create audio folder if it doesn't exist
os.makedirs(audio_folder, exist_ok=True)

# Load model and processor
model = AutoModel.from_pretrained(
    "m-a-p/MERT-v1-330M", trust_remote_code=True, output_hidden_states=True
).to(cuda)
processor = Wav2Vec2FeatureExtractor.from_pretrained(
    "m-a-p/MERT-v1-330M", trust_remote_code=True
)

# Ensure sample rate alignment
resample_rate = processor.sampling_rate
if resample_rate != sampling_rate:
    print(f"Setting rate from {sampling_rate} to {resample_rate}")

# Define the resampler
resampler = T.Resample(
    orig_freq=sampling_rate,
    new_freq=resample_rate,
).to(cuda)

aggregator = nn.Conv1d(in_channels=25, out_channels=1, kernel_size=1).to(
    cuda
)  # ? Model: 330M
# aggregator = nn.Conv1d(in_channels=13, out_channels=1, kernel_size=1).to(
#     cuda
# )  # ? Model: 95M

# Queue for buffering songs
song_queue = Queue(maxsize=queue_size)
write_queue = Queue()

# Load processed IDs
if os.path.exists(ids_file_path):
    with open(ids_file_path, "r") as f:
        processed_ids = set(f.read().splitlines())
else:
    processed_ids = set()


def download_songs():
    with open(csv_file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            track_id = row["track_id"]
            track_preview_url = row["track_preview_url"]
            if not track_preview_url or track_id in processed_ids:
                continue

            print(f"Downloading: {track_id}")
            audio_file = requests.get(track_preview_url)
            song = pydub.AudioSegment.from_file(io.BytesIO(audio_file.content))
            song_path = os.path.join(audio_folder, f"{track_id}.wav")
            download_song(song, track_id, song_path)


def download_song(song, track_id, song_path):
    song.export(song_path, format="wav")
    song_queue.put((track_id, song_path))
    print(f"Downloaded and buffered: {song_path}")


def create_embeddings_worker(event):
    while not event.is_set():
        item = song_queue.get()
        if item is None:
            break

        track_id, song_path = item

        dataset = Dataset.from_dict(
            {
                "audio": [song_path],
                "id": [track_id],
            }
        ).cast_column("audio", Audio())
        row = dataset[0]

        waveform = torch.from_numpy(row["audio"]["array"]).float().to(cuda)
        print(f"Resampling: {song_path} (CUDA: {waveform.is_cuda})")
        waveform = resampler(waveform)

        print(f"Extracting features: {song_path} (CUDA: {waveform.is_cuda})")
        inputs = processor(
            waveform, sampling_rate=resample_rate, return_tensors="pt"
        ).to(cuda)
        print(f"Create embedding: {song_path} (CUDA: {inputs.input_values.is_cuda})")
        with torch.no_grad():
            outputs = model(**inputs, output_hidden_states=True)

        print(
            f"Additional processing: {song_path} (CUDA: {outputs.last_hidden_state.is_cuda})"
        )
        all_layer_hidden_states = torch.stack(outputs.hidden_states).squeeze()
        time_reduced_hidden_states = all_layer_hidden_states.mean(-2)
        print(f"Aggregating: {song_path} (CUDA: {time_reduced_hidden_states.is_cuda})")

        weighted_avg_hidden_states = aggregator(time_reduced_hidden_states)

        print(
            f"Saving embedding: {song_path} (CUDA: {weighted_avg_hidden_states.is_cuda})"
        )

        embedding = weighted_avg_hidden_states.cpu().detach().numpy()
        embedding = embedding.reshape(-1)
        write_queue.put((embedding, track_id, song_path))

        print(f"Processed: {song_path}")

        song_queue.task_done()


def write_worker():
    while True:
        item = write_queue.get()
        if item is None:
            break
        print("Write queue: ", write_queue.qsize())

        (
            embedding,
            track_id,
            song_path,
        ) = item

        print(f"Writing embedding: {song_path}")

        if not os.path.exists(embedding_file):
            np.save(embedding_file, np.array([embedding]))
        else:
            with NpyAppendArray(embedding_file) as data:
                data.append(np.array([embedding]))

        if not os.path.exists(embedding_id_file):
            np.save(embedding_id_file, np.array([track_id]))
        else:
            with NpyAppendArray(embedding_id_file) as data:
                data.append(np.array([track_id]))

        with open(ids_file_path, "a") as f:
            f.write(f"{track_id}\n")

        os.remove(song_path)
        print(f"Deleted: {song_path}")

        write_queue.task_done()


def main():
    """
    We have 3 types of workers:
    1. Download songs
    2. Create embeddings
    3. Write embeddings

    Download songs and write embeddings are in one thread each
    Create embeddings is in multiple threads

    The main function will start all workers and wait for them to finish OR
    until the user interrupts the process. It will then join all threads and
    cleanup.
    """

    download_thread = threading.Thread(target=download_songs)
    download_thread.start()

    event = threading.Event()
    create_threads = []
    for i in range(n_threads):
        create_thread = threading.Thread(
            target=create_embeddings_worker, name=f"embedding-{i}", args=(event,)
        )
        create_thread.start()
        create_threads.append(create_thread)

    write_thread = threading.Thread(target=write_worker)
    write_thread.start()

    try:
        download_thread.join()
        for create_thread in create_threads:
            create_thread.join()
        write_thread.join()
    except KeyboardInterrupt:
        event.set()

        download_thread.join()
        for create_thread in create_threads:
            create_thread.join()
        write_thread.join()

    print("All threads joined.")
    print("Exiting...")
    return


if __name__ == "__main__":
    main()
