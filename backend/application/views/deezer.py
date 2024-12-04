from rest_framework.decorators import api_view
from django.apps import apps
import logging
import pandas
from django.core.paginator import Paginator
from django.http import JsonResponse
import deezer
import requests

DEEZER_URL = "https://api.deezer.com"
TRACK_URL = f"{DEEZER_URL}/track"
SEARCH_URL = f"{DEEZER_URL}/search"
PLAYLIST_URL = f"{DEEZER_URL}/playlist"

def get_playlist(playlist_id):
    print(f"Getting playlist from : {PLAYLIST_URL}/{playlist_id}")

    response = requests.get(f"{PLAYLIST_URL}/{playlist_id}")

    response.raise_for_status()

    return response.json()

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
    print(f"Getting track from : {TRACK_URL}/{track_id}")

    response = requests.get(f"{TRACK_URL}/{track_id}")

    response.raise_for_status()

    return response.json()

@api_view(["GET"])
def track_view(request):
    track_id = request.GET.get("track_id", "")

    if track_id == "":
        return JsonResponse({"error": "No track identifier provided"}, status=400)

    try:
        track = get_track(track_id)
    except Exception as e:
        return JsonResponse({str(e)}, status=500)

    print(f"Track : {track}")

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
