from rest_framework.decorators import api_view
from django.apps import apps
import pandas
import logging
from django.http import JsonResponse
import numpy
from transformers import AutoModel, Wav2Vec2FeatureExtractor
import torch
import torchaudio
import requests

from . import spotify

CONFIGURATION = apps.get_app_config("application")

EMBEDDINGS = None

DEVICE = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
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

def load_embeddings():
    try:
        embeddings = numpy.load(f"{CONFIGURATION.data_path}/embeddings_330.npy")
        id = numpy.load(f"{CONFIGURATION.data_path}/id_embeddings_330.npy")

        return {"embeddings": embeddings, "identifiers": id}

    except FileNotFoundError:
        logging.error("Embeddings file not found")
        raise FileNotFoundError
    except Exception as e:
        logging.error(f"Error loading embeddings: {e}")
        raise e


def get_embeddings():
    global EMBEDDINGS

    if EMBEDDINGS is None:
        EMBEDDINGS = load_embeddings()

    return EMBEDDINGS


def get_cosine_similarity(embeddings, embedding):
    cosine_similarities = numpy.dot(embeddings, embedding) / (
        numpy.linalg.norm(embeddings, axis=1) * numpy.linalg.norm(embedding)
    )

    nearest_indices = numpy.argsort(cosine_similarities)[::-1][1:6]

    return

def download_track(preview_url):
    response = requests.get(preview_url)

    if response.status_code != 200:
        return None

    return response.content
        



@api_view(["GET"])
def compose_view(request):

    print(request.GET)

    track_id = request.GET.get("track_id", "")
    
    if track_id == "":
        return JsonResponse({"error": "No track specified"})

    logging.info(f"Downloading track {track_id}")
    
    track_url = spotify.SPOTIFY.audio_features([track_id])
    
    print(track_url)

#    logging.info(f"Composing for track {track}")

    embeddings = get_embeddings()

    print(embeddings["identifiers"][0])

    return JsonResponse({"embeddings": "embeddings"})
