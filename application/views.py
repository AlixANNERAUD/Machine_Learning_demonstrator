from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.apps import apps
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import plotly.express as px
import numpy
import spotipy

configuration = apps.get_app_config("application")


# Create your views here.
def home_view(request):
    return render(request, "application.html")


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

    tracks = page.object_list[["release_date", "track_name", "artists", "track_duration_ms"]]

    return render(
        request, "tracks.html", {"tracks": tracks, "page": page, "search": search, "total_tracks": paginator.count}
    )


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

    plot_html = figure.to_html(
        full_html=False, default_height="100%", default_width="100%"
    )

    return render(request, "umap.html", {"plot": plot_html})


def get_spotify_authenticator(request):
    cache_handler = spotipy.cache_handler.DjangoSessionCacheHandler(request)

    spotify_authenticator = spotipy.oauth2.SpotifyOAuth(
        client_id=configuration.spotify_client_id,
        client_secret=configuration.spotify_client_secret,
        redirect_uri=f"http://{request.get_host()}/spotify",
        scope="user-library-read",
        cache_handler=cache_handler,
        show_dialog=True,
        open_browser=False,
    )

    return (cache_handler, spotify_authenticator)


def get_spotify_client(request):
    _, spotify_authenticator = get_spotify_authenticator(request)

    return spotipy.Spotify(auth_manager=spotify_authenticator)


def spotify_view(request):
    cache_handler, spotify_authenticator = get_spotify_authenticator(request)

    # If the code is in the request GET parameters, get the access token
    if request.GET.get("code"):
        spotify_authenticator.get_access_token(request.GET.get("code"))

    # If the token is not valid, redirect to the Spotify login page
    if not spotify_authenticator.validate_token(cache_handler.get_cached_token()):
        authentication_url = spotify_authenticator.get_authorize_url()
        return redirect(authentication_url)

    spotify_client = spotipy.Spotify(auth_manager=spotify_authenticator)

    return redirect("Account")


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

    return render(
        request,
        "account.html",
        {"user_data": user_data, "playlists": playlists["items"]},
    )
