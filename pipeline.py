import csv
import io
import os
import threading
from concurrent.futures import ThreadPoolExecutor
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

cuda = torch.device("cuda")

song_buffer_size = 5
n_threads = 8
queue_size = 10

csv_file_path = "tracks.csv"
audio_folder = "audio"
ids_file_path = "processed_ids.txt"
embedding_file = "embeddings.npy"
embedding_id_file = f"id_{embedding_file}"
sampling_rate = 44100

# Create audio folder if it doesn't exist
os.makedirs(audio_folder, exist_ok=True)

# Load model and processor
model = AutoModel.from_pretrained(
    "m-a-p/MERT-v1-330M", trust_remote_code=True, output_hidden_states=True
)
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

aggregator = nn.Conv1d(in_channels=25, out_channels=1, kernel_size=1)

# Queue for buffering songs
song_queue = Queue(maxsize=queue_size)

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

        waveform = row["audio"]["array"]
        print(f"Resampling: {song_path}")
        waveform = resampler(torch.from_numpy(waveform).float().to(cuda))

        print(f"Extracting features: {song_path}")
        inputs = processor(waveform, sampling_rate=resample_rate, return_tensors="pt")
        print(f"Create embedding: {song_path}")
        with torch.no_grad():
            outputs = model(**inputs, output_hidden_states=True)

        print(f"Additional processing: {song_path}")
        all_layer_hidden_states = torch.stack(outputs.hidden_states).squeeze()
        time_reduced_hidden_states = all_layer_hidden_states.mean(-2)
        weighted_avg_hidden_states = aggregator(
            time_reduced_hidden_states.unsqueeze(0)
        ).squeeze()

        embedding = weighted_avg_hidden_states.detach().numpy()

        if not os.path.exists(embedding_file):
            np.save(embedding_id_file, np.array([track_id]))
            np.save(embedding_file, np.array([embedding]))
        else:
            with NpyAppendArray(embedding_file) as data:
                data.append(np.array([embedding]))

            with NpyAppendArray(embedding_id_file) as data:
                data.append(np.array([track_id]))

        print(f"Created embedding for: {song_path}")

        # Mark the track as processed
        with open(ids_file_path, "a") as f:
            f.write(f"{track_id}\n")

        # Delete the audio file
        os.remove(song_path)
        print(f"Deleted: {song_path}")

        song_queue.task_done()


def create_embeddings(n_threads):
    event = threading.Event()
    with ThreadPoolExecutor(max_workers=n_threads) as executor:
        for _ in range(n_threads):
            executor.submit(create_embeddings_worker, event)

    # Wait for the queue to be empty
    song_queue.join()
    event.set()


# Start the download thread
download_thread = threading.Thread(target=download_songs, daemon=True)
download_thread.start()

# Example usage
create_embeddings(n_threads)

# Wait for the download thread to finish
download_thread.join()

# Signal the embedding thread to finish
song_queue.put(None)

print("Pipeline completed.")
