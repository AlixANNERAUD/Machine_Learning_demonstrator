from queue import Queue
from rest_framework.decorators import api_view
from django.apps import apps
import logging
import threading
from django.http import JsonResponse
import threading

from . import deezer, processing, data

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

        print(f"Downloading track {track_id}")

        # Get the track metadata
        try:
            metadata = deezer.get_track(track_id)
        except Exception as e:
            logging.error(f"Error downloading track {track_id}: {e}")
            continue
        
        if metadata["preview"] == "":
            logging.info(f"No preview url for track : {metadata['preview']}")
            continue
        
            
        # Download the track
        path = processing.download_track(track_id, metadata["preview"])

        print(f"download : ")

        # Add the track id, path and metadata to the embedding queue
        EMBEDDING_QUEUE.put((track_id, path, metadata))

        # Mark the task as done
        DOWNLOAD_QUEUE.task_done()


def embedding_worker():
    while True:
        # Get the track id, path and metadata from the queue (this will block until a track is available)
        track_id, path, metadata = EMBEDDING_QUEUE.get(block=True)

        print(f"Embedding track {track_id}")

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

        print(f"Saving track {track_id}")

        # Add the track to the dataset
        data.add_track(track_id, embedding, metadata)

        # Mark the task as done
        SAVE_QUEUE.task_done()

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

    playlist_id = request.GET.get("playlist_id", "")

    if playlist_id != "":
        try:
            playlist = deezer.get_playlist(playlist_id)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

        for track in playlist["tracks"]["data"]:
            track_id = track["id"]
            DOWNLOAD_QUEUE.put(track_id)

        return JsonResponse({"message": "Downloading tracks"})

    track_id = request.GET.get("track_id", "")

    if track_id != "":
        DOWNLOAD_QUEUE.put(track_id)

        return JsonResponse({"message": "Downloading track"})


def start_workers():
    global DOWNLOAD_THREAD, EMBEDDING_THREAD

    if DOWNLOAD_THREAD is not None and EMBEDDING_THREAD is not None and SAVE_THREAD is not None:
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
