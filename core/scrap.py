import csv
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

------- Tracks file format --------
CSV file with the following columns:
album_id            release_date        release_date_precision
album_restrictions  track_id            track_name
track_duration_ms   track_explicit      track_restrictions
track_popularity    track_preview_url   acousticness
analysis_url        danceability        energy
instrumentalness    key                 liveness
loudness            mode                speechiness
tempo               time_signature      valence
artists
-----------------------------------
"""


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
    data["queued_playlists"].remove(playlist_id)

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


def load_seen_track_file(filename: str) -> object:
    """
    Load seen tracks from a file

    :param filename: File to load from (CSV)
    :return: Set of seen track IDs"""

    return open(filename, "a+", newline="")


def unload_seen_track_file(file: object):
    """
    Unload a seen track file

    :param file: File to unload
    """

    file.close()


def save_seen_track(track: object, file):
    """
    Save a track to the seen tracks file (CSV)

    :param track: Track object
    :param file: File to save to (CSV)
    """

    writer = csv.DictWriter(file, fieldnames=track.keys())

    if file.tell() == 0:
        writer.writeheader()

    writer.writerow(track)


def check_seen_track(track_id: str, file) -> bool:
    """
    Check if a track has been seen before

    :param track: Track object
    :param file: File to load from (CSV)
    :return: True if track has been seen before, False otherwise
    """

    file.seek(0)

    reader = csv.DictReader(file)

    for row in reader:
        if row["track_id"] == track_id:
            return True
    return False
