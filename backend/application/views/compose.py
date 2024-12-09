from rest_framework.decorators import api_view
from django.apps import apps
import logging
from django.http import JsonResponse
import requests
from . import processing
from . import data
from . import deezer

CONFIGURATION = apps.get_app_config("application")


@api_view(["GET"])
def compose_view(request):
    # Get the parameters from the request
    track_id = request.GET.get("track_id", "")
    results = int(request.GET.get("results", "10"))

    # Check if the track_id is empty
    if track_id == "":
        return JsonResponse({"error": "No track specified"}, status=400)

    # Try to get the embedding from the data
    try:
        metadata, embedding = data.get_track(track_id)
    # If the embedding is not found, download the track, create the embedding and add it to the data
    except KeyError:
        metadata = deezer.get_track(track_id)
        
        logging.info(f"Downloading track {track_id}")

        path = processing.download_track(track_id, metadata["preview"])

        logging.info(f"Creating embedding for track {track_id}")

        embedding = processing.compute_embedding(track_id, path)

        logging.info(f"Adding embedding for track {track_id}")

        data.add_track(track_id, embedding, metadata)
        
        data.save()

    # Get the similar tracks
    logging.info(f"Getting cosine similarity for track {track_id}")

    similar_tracks = processing.get_similar_tracks(embedding, results=results)

    print(f"Similar tracks {similar_tracks}")

    return JsonResponse({"similar_tracks": similar_tracks})
