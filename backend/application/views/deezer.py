from rest_framework.decorators import api_view
from django.apps import apps
import logging
import pandas
from django.core.paginator import Paginator
from django.http import JsonResponse
import requests
import time

from . import data

DEEZER_URL = "https://api.deezer.com"
TRACK_URL = f"{DEEZER_URL}/track"
SEARCH_URL = f"{DEEZER_URL}/search"
PLAYLIST_URL = f"{DEEZER_URL}/playlist"
ALBUM_URL = f"{DEEZER_URL}/album"
GENRE_URL = f"{DEEZER_URL}/genre"

def get_genre(genre_id):
    response = requests.get(f"{GENRE_URL}/{genre_id}")
    
    response.raise_for_status()
    
    return response.json()

def get_album(album_id):
    response = requests.get(f"{ALBUM_URL}/{album_id}")

    response.raise_for_status()

    return response.json()


def get_playlist(playlist_id, index=None, limit=None):
    parameters = {}

    if index is not None:
        parameters["index"] = index

    if limit is not None:
        parameters["limit"] = limit

    response = requests.get(f"{PLAYLIST_URL}/{playlist_id}", params=parameters)

    response.raise_for_status()

    return response.json()

def get_all_playlist_tracks(playlist_id):
    tracks = []
    index = 0
    limit = 400

    while True:
        playlist = get_playlist(playlist_id, index=index, limit=limit)
    
        if "tracks" not in playlist:
            break

        tracks += playlist["tracks"]["data"]

        if len(playlist["tracks"]["data"]) < limit:
            break

        index += limit

    return tracks

@api_view(["GET"])
def playlist_view(request):
    playlist_id = request.GET.get("playlist_id", "")

    if playlist_id == "":
        return JsonResponse({"error": "No playlist identifier provided"}, status=400)

    try:
        playlist = get_playlist(playlist_id)
    except Exception as e:
        return JsonResponse({str(e)}, status=500)

    return JsonResponse(playlist)


def get_track(track_id):
    response = requests.get(f"{TRACK_URL}/{track_id}")

    response.raise_for_status()

    return response.json()

@api_view(["GET"])
def genre_view(request):
    genre_id = request.GET.get("genre_id", "")

    if genre_id == "":
        return JsonResponse({"error": "No genre identifier provided"}, status=400)

    try:
        genre = get_genre(genre_id)
    except Exception as e:
        return JsonResponse({str(e)}, status=500)

    return JsonResponse(genre)

@api_view(["GET"])
def track_view(request):
    track_id = request.GET.get("track_id", "")

    if track_id == "":
        return JsonResponse({"error": "No track identifier provided"}, status=400)

    try:
        track, _ = data.get_track(track_id)

        return JsonResponse(track)
    except KeyError:
        pass

    try:
        track = get_track(track_id)
    except Exception as e:
        return JsonResponse({str(e)}, status=500)

    return JsonResponse(track)


@api_view(["GET"])
def search_view(request):

    query = request.GET.get("query", "")

    if query == "":
        return JsonResponse({"error": "No query provided"}, status=400)

    response = requests.get(SEARCH_URL, params={"q": query})

    try:
        response.raise_for_status()
    except Exception as e:
        return JsonResponse({str(e)}, status=500)

    return JsonResponse(response.json())
