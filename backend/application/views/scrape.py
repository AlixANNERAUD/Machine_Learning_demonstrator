from queue import Queue
from rest_framework.decorators import api_view
from django.apps import apps
import logging
import threading

from . import deezer, processing

CONFIGURATION = apps.get_app_config("application")

DOWNLOAD_QUEUE = Queue()
EMBEDDING_QUEUE = Queue()

DOWNLOAD_THREAD = None
EMBEDDING_THREAD = None


def download_worker():
    while True:
        # Get the track id from the queue (this will block until a track is available)
        track_id = DOWNLOAD_QUEUE.get(block=True)

        # Get the track metadata
        try:
            metadata = deezer.get_track(track_id)
        except Exception as e:
            logging.error(f"Error downloading track {track_id}: {e}")
            continue

        # Download the track
        path = deezer.download_track(track_id, metadata["preview"])

        # Add the track id, path and metadata to the embedding queue
        EMBEDDING_QUEUE.put((track_id, path, metadata))

        # Mark the task as done
        DOWNLOAD_QUEUE.task_done()


def embedding_worker():
    while True:
        # Get the track id, path and metadata from the queue (this will block until a track is available)
        track_id, path, metadata = EMBEDDING_QUEUE.get(block=True)

        # Compute the embedding
        try:
            embedding = processing.compute_embedding(track_id, path)
        except Exception as e:
            logging.error(f"Error embedding track {track_id}: {e}")
            continue
        
        # Add the track to the dataset
        data.add_track(track_id, embedding, metadata)
        
        # Mark the task as done
        EMBEDDING_QUEUE.task_done()

@api_view(["GET"])
def scrape_view(request):

    playlist_id = request.GET.get("playlist_id", "")

    if playlist_id != "":
        try:
            playlist = deezer.get_playlist(playlist_id)
        except Exception as e:
            return JsonResponse({str(e)}, status=500)

        for track in playlist["tracks"]:
            track_id = track["id"]
            DOWNLOAD_QUEUE.put(track_id)

        return JsonResponse({"message": "Downloading tracks"})

    track_id = request.GET.get("track_id", "")

    if track_id != "":
        DOWNLOAD_QUEUE.put(track_id)

        return JsonResponse({"message": "Downloading track"})
