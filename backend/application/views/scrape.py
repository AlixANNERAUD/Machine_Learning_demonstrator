import logging
import threading
from queue import Queue

from django.apps import apps
from django.http import JsonResponse
from rest_framework.decorators import api_view
from urllib3.exceptions import MaxRetryError

from . import data, deezer, processing

CONFIGURATION = apps.get_app_config("application")

DOWNLOAD_QUEUE = Queue()
EMBEDDING_QUEUE = Queue()
SAVE_QUEUE = Queue()

DOWNLOAD_THREAD = None
EMBEDDING_THREAD = None
SAVE_THREAD = None


def download_worker():
    while True:
        # Get the track id from the queue (this will block until a track is available)
        track_id = DOWNLOAD_QUEUE.get(block=True)

        # Check if the track is already in the dataset
        if data.track_exists(track_id):
            continue

        # Get the track metadata
        try:
            metadata = deezer.get_track(track_id)
        except Exception as e:
            logging.error(f"Error downloading track {track_id}: {e}")
            continue

        print(f"Downloading track {metadata}")

        if metadata["preview"] == "":
            logging.info(f"No preview url for track : {track_id}")
            continue

        # Download the track
        try:
            path = processing.download_track(track_id, metadata["preview"])
        except MaxRetryError as e:
            logging.error(f"You are being rate limited by Deezer API: {e}")
            exit(1)

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
        SAVE_QUEUE.put((track_id, embedding, metadata))

        # Mark the task as done
        EMBEDDING_QUEUE.task_done()


def save_worker():
    while True:
        # Get the track id, embedding and metadata from the queue (this will block until a track is available)
        track_id, embedding, metadata = SAVE_QUEUE.get(block=True)

        # Check if album is already in the dataset
        try:
            data.get_album(metadata["album"]["id"])
        except KeyError:
            album = deezer.get_album(metadata["album"]["id"])
            data.add_album(metadata["album"]["id"], album)

        # Add the track to the dataset
        data.add_track(track_id, embedding, metadata)

        # Mark the task as done
        SAVE_QUEUE.task_done()

        # If the queue is empty, save the dataset
        if SAVE_QUEUE.empty():
            data.save()


@api_view(["GET"])
def queues_view(request):
    download_queue = list(DOWNLOAD_QUEUE.queue)

    embedding_queue = [track_id for track_id, _, _ in EMBEDDING_QUEUE.queue]

    return JsonResponse(
        {
            "download_queue": download_queue,
            "embedding_queue": embedding_queue,
        }
    )


@api_view(["GET"])
def scrape_view(request):
    # Get the parameters from the request
    playlist_id = request.GET.get("playlist_id", "")

    if playlist_id != "":
        # Get all the tracks from the playlist
        try:
            tracks = deezer.get_all_playlist_tracks(playlist_id)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        print(f"Downloading {len(tracks)} tracks")

        # Add the tracks to the download queue if they are not already in the dataset
        for track in tracks:
            if not data.track_exists(track["id"]):
                DOWNLOAD_QUEUE.put(track["id"])

        # Tell the user that the tracks are being downloaded
        return JsonResponse({"message": "Downloading tracks"})

    track_id = request.GET.get("track_id", "")

    # Check if the track_id is empty
    if track_id != "":
        if data.track_exists(track_id):
            return JsonResponse({"message": "Track already downloaded"})
        else:
            DOWNLOAD_QUEUE.put(track_id)
            return JsonResponse({"message": "Downloading track"})


def start_workers():
    global DOWNLOAD_THREAD, EMBEDDING_THREAD

    if (
        DOWNLOAD_THREAD is not None
        and EMBEDDING_THREAD is not None
        and SAVE_THREAD is not None
    ):
        return

    DOWNLOAD_THREAD = threading.Thread(target=download_worker)
    DOWNLOAD_THREAD.start()

    EMDEDING_THREAD = []
    for thread in range(4):
        EMDEDING_THREAD = threading.Thread(target=embedding_worker)
        EMDEDING_THREAD.start()

    EMBEDDING_THREAD = threading.Thread(target=save_worker)
    EMBEDDING_THREAD.start()


start_workers()
