from django.apps import apps
from datasets import Audio, Dataset
import os
import pydub
import io
import numpy
from transformers import AutoModel, Wav2Vec2FeatureExtractor
import torch
import torchaudio
import requests
import logging
from . import data
import pandas


CONFIGURATION = apps.get_app_config("application")

if torch.cuda.is_available():
    logging.info("Using CUDA")
    DEVICE = torch.device("cuda")
else:
    logging.info("Using CPU")
    DEVICE = torch.device("cpu")

MODEL = AutoModel.from_pretrained(
    "m-a-p/MERT-v1-330M", trust_remote_code=True, output_hidden_states=True
).to(DEVICE)
EXTRACTOR = Wav2Vec2FeatureExtractor.from_pretrained(
    "m-a-p/MERT-v1-330M", trust_remote_code=True
)

SPOTIFY_SAMPLING_RATE = 44100
EXTRACTOR_SAMPLING_RATE = EXTRACTOR.sampling_rate
RESAMPLER = torchaudio.transforms.Resample(
    orig_freq=SPOTIFY_SAMPLING_RATE, new_freq=EXTRACTOR_SAMPLING_RATE
).to(DEVICE)

AGGREGATOR = torch.nn.Conv1d(in_channels=25, out_channels=1, kernel_size=1).to(DEVICE)

def download_track(track_id, preview_url):
    # Create the audio path if it doesn't exist
    os.makedirs(CONFIGURATION.audio_path, exist_ok=True)

    # Download the track
    response = requests.get(preview_url)
    if response.status_code != 200:
        raise Exception(f"Failed to download track: {response.status_code}")

    # Convert the track to an audio segment
    audio_file = pydub.AudioSegment.from_file(io.BytesIO(response.content))

    # Convert the track to a wav file
    path = os.path.join(CONFIGURATION.audio_path, f"{track_id}.mp3")
    audio_file.export(path, format="wav")

    return path


def compute_embedding(track_id, path):
    # Load the datset
    dataset = Dataset.from_dict(
        {
            "audio": [path],
            "id": [track_id],
        }
    ).cast_column("audio", Audio())

    # Get the first row
    row = dataset[0]

    # Load the audio file
    waveform = torch.from_numpy(row["audio"]["array"]).float().to(DEVICE)

    # Resample the audio file
    waveform = RESAMPLER(waveform)

    # Extract the features
    inputs = EXTRACTOR(
        waveform, sampling_rate=EXTRACTOR_SAMPLING_RATE, return_tensors="pt"
    ).to(DEVICE)

    # Create the embedding
    with torch.no_grad():
        outputs = MODEL(**inputs, output_hidden_states=True)

    # Aggregate the embeddings
    all_layer_hidden_states = torch.stack(outputs.hidden_states).squeeze()
    time_reduced_hidden_states = all_layer_hidden_states.mean(-2)

    weighted_average_hidden_states = AGGREGATOR(time_reduced_hidden_states)

    # Load back to CPU
    embedding = weighted_average_hidden_states.cpu().detach().numpy()
    embedding = embedding.reshape(-1)

    # Delete the audio file
    os.remove(path)

    return embedding


def get_cosine_similarity(embeddings, embedding, results=5):
    # Calculate the cosine similarity between the embeddings
    cosine_similarities = numpy.dot(embeddings, embedding) / (
        numpy.linalg.norm(embeddings, axis=1) * numpy.linalg.norm(embedding)
    )

    # Get the nearest indices
    nearest_indexes = numpy.argsort(cosine_similarities)[::-1][1:results]

    return nearest_indexes

def get_similar_tracks(embedding, results=5):  
    embeddings = data.get_embeddings()
    identifiers = data.get_identifiers()

    nearest_indexes = get_cosine_similarity(
        embeddings, embedding, results=results
    )

    return identifiers[nearest_indexes].tolist()
