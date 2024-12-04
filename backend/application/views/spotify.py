from django.apps import apps
import spotipy

CONFIGURATION = apps.get_app_config("application")

SPOTIFY = spotipy.Spotify(
    auth_manager=spotipy.SpotifyClientCredentials(
        client_id=CONFIGURATION.spotify_client_id,
        client_secret=CONFIGURATION.spotify_client_secret,
    )
)
