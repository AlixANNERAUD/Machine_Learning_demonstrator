from rest_framework.decorators import api_view
from django.apps import apps
import pandas
import logging
from django.http import JsonResponse
import numpy

configuration = apps.get_app_config("application")

EMBEDDINGS = None


def load_embeddings():
    try:
        embeddings = numpy.load(f"{configuration.data_path}/embeddings_330.npy")
        id = numpy.load(f"{configuration.data_path}/id_embeddings_330.npy")

        return {embeddings, id_embeddings}

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


@api_view(["GET"])
def compose_view(request):

    track = request.GET.get("track", "")

    if track == "":
        return JsonResponse({"error": "No track specified"})

    logging.info(f"Composing for track {track}")

    embeddings = get_embeddings()

    return JsonResponse({"embeddings": "embeddings"})
