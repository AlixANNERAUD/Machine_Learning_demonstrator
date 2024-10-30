import os

import spotipy
import spotipy.exceptions

"""
------ Playlists file format ------
{
    "seen_playlists": [...],
    "queued_playlists": [...]
}
-----------------------------------


def load_spotify_client() -> spotipy.Spotify:
    """
    Load Spotify client with credentials from environment variables

    :return: Spotify client

    :raises ValueError: If Spotify API keys are missing
    """

    try:
        from dotenv import load_dotenv

        load_dotenv()
    except ImportError:
        pass

    # Load API keys from environment variables
    client_id = os.getenv("SPOTIPY_CLIENT_ID")
    client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

    # Check if API keys are set
    if not client_id or not client_secret:
        raise ValueError("Spotify API keys are missing")

    # Authenticate with Spotify API
    auth_manager = spotipy.SpotifyClientCredentials(
        client_id=client_id, client_secret=client_secret
    )
    return spotipy.Spotify(auth_manager=auth_manager)

