from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.apps import apps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import plotly.express as px
import numpy
import spotipy
from django.views.decorators.csrf import ensure_csrf_cookie
from django.http import JsonResponse
from rest_framework.decorators import api_view

configuration = apps.get_app_config("application")


# Create your views here.
def home_view(request):
    return render(request, "application.html")


@api_view(["GET"])
def tracks_view(request):
    search = request.GET.get("search", "")

    if search == "":
        tracks = configuration.tracks
    else:
        tracks = configuration.tracks[
            configuration.tracks["track_name"].str.contains(
                search, case=False, na=False
            )
        ]

    paginator = Paginator(tracks, 100)

    page_number = request.GET.get("page", 1)

    page = paginator.get_page(page_number)

    total_pages = paginator.num_pages
    current_page = page_number

    tracks = page.object_list[
        ["release_date", "track_name", "artists", "track_duration_ms"]
    ]

    return JsonResponse(
        {
            "tracks": tracks.to_dict(orient="records", index=True),
            "total_pages": total_pages,
            "current_page": current_page,
        }
    )


@api_view(["GET"])
def umap_view(request):
    figure = px.scatter_3d(
        configuration.umap[["x", "y", "z"]],
        x="x",
        y="y",
        z="z",
        color=numpy.linspace(0, 1, configuration.umap.shape[0]),
    )

    figure.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
    )

    data = {
        "x": configuration.umap["x"].to_list(),
        "y": configuration.umap["y"].to_list(),
        "z": configuration.umap["z"].to_list(),
    }

    return JsonResponse(data)


def get_spotify_client(request):
    _, spotify_authenticator = get_spotify_authenticator(request)

    return spotipy.Spotify(auth_manager=spotify_authenticator)


def spotify_view(request):

    redirect_uri = request.GET.get(
        "redirect_uri", request.build_absolute_uri("/spotify/")
    )

    cache_handler, spotify_authenticator = get_spotify_authenticator(
        request, redirect_uri
    )

    # If the code is in the request GET parameters, get the access token
    if request.GET.get("code"):
        spotify_authenticator.get_access_token(request.GET.get("code"))

    # If the token is not valid, redirect to the Spotify login page
    if not spotify_authenticator.validate_token(cache_handler.get_cached_token()):
        authentication_url = spotify_authenticator.get_authorize_url()
        return redirect(authentication_url)

    spotify_client = spotipy.Spotify(auth_manager=spotify_authenticator)

    return redirect("/")


@api_view(["GET"])
def me(request):
    cache_handler, spotify_authenticator = get_spotify_authenticator(request)

    if not spotify_authenticator.validate_token(cache_handler.get_cached_token()):
        return

    spotify_client = get_spotify_client(request)

    return JsonResponse(spotify_client.me())


def authenticate(request):
    cache_handler, spotify_authenticator = get_spotify_authenticator(request)

    if not spotify_authenticator.validate_token(cache_handler.get_cached_token()):
        return redirect("Spotify")

    return redirect("/")


def account_view(request):
    cache_handler, spotify_authenticator = get_spotify_authenticator(request)

    if not spotify_authenticator.validate_token(cache_handler.get_cached_token()):
        return redirect("Spotify")

    spotify_client = get_spotify_client(request)

    # If the user data is not in the session, get it from the Spotify API
    if request.session.get("user_data") is None:
        request.session["user_data"] = spotify_client.me()

    # If the playlists are not in the session, get them from the Spotify API
    if request.session.get("playlists") is None:
        request.session["playlists"] = spotify_client.current_user_playlists(limit=100)

    user_data = request.session["user_data"]
    playlists = request.session["playlists"]

    return JsonResponse(
        {
            "user_data": user_data,
            "playlists": playlists,
        }
    )


@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({"detail": "CSRF cookie set"})
