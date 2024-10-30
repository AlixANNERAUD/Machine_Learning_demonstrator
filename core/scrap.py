import json
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


def save_seen_playlists(playlist_id: str, filename: str):
    """
    Save a playlist ID to the seen playlists file

    :param playlist_id: Playlist ID
    :param filename: File to save to (json)"""

    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {"seen_playlists": [], "queued_playlists": []}

    data["seen_playlists"].append(playlist_id)

    with open(filename, "w") as file:
        json.dump(data, file)


def load_seen_playlists(filename: str) -> set[str]:
    """
    Load seen playlists from a file

    :param filename: File to load from (json)
    :return: Set of seen playlist IDs
    """

    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return set()

    return set(data["seen_playlists"] if "seen_playlists" in data else [])


def load_queued_playlists(filename: str) -> set[str]:
    """
    Load queued playlists from a file

    :param filename: File to load from (json)
    :return: Set of queued playlist IDs
    """

    try:
        with open(filename, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return set()

    return set(data["queued_playlists"] if "queued_playlists" in data else [])


def check_seen_playlist(playlist_id: str, filename: str) -> bool:
    """
    Check if a playlist has been seen before

    :param playlist_id: Playlist ID
    :param filename: File to load from (json)
    :return: True if playlist has been seen before, False otherwise
    """

    return playlist_id in load_seen_playlists(filename)

