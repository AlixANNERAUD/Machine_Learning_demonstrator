import csv
import os
import random
import time

from spotipy.exceptions import SpotifyException

from modules import scrap

# Load API keys from environment variables
sp = scrap.load_spotify_client()


# Handle API exceptions and request limits
def handle_spotify_exception(e):
    if isinstance(e, SpotifyException):
        if e.http_status == 429:  # Rate limit exceeded
            retry_after = int(e.headers.get("Retry-After", 250))
            print(f"Rate limit hit, waiting for {retry_after} seconds...")
            time.sleep(retry_after)
            return True
        elif e.http_status == 404:  # Resource not found
            print("Resource not found, skipping to next...")
            return False
    else:
        print(f"Unknown error: {e}")
        return False


# Get all tracks from a playlist
def get_all_playlist_tracks(playlist_id):
    all_tracks = []
    offset = 0
    limit = 100  # Spotify limits tracks per request to 100

    while True:
        try:
            response = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
            tracks = response["items"]
            all_tracks.extend(tracks)

            print(f"Added (playlist): {len(tracks)} tracks ({len(all_tracks)})")

            # Break when no more tracks to fetch
            if len(tracks) < limit:
                break

            # Increase offset to fetch the next batch
            offset += limit
        except SpotifyException as e:
            if not handle_spotify_exception(e):
                break

    return all_tracks


# Main function to scrape a playlist
def scrape_playlist(playlist_id, csv):
    if scrap.check_seen_playlist(playlist_id, "playlists.json"):
        print(f"Playlist {playlist_id} already seen, skipping...")
        return

    # Get all the tracks from the playlist
    all_tracks = get_all_playlist_tracks(playlist_id)
    print(f"Found {len(all_tracks)} tracks in the playlist")

    track_ids = []
    for item in all_tracks:
        track = item.get("track")  # Safely get 'track' from the item

        # Check if the track is None (e.g., removed or invalid track)
        if track is None:
            print(f"Track is missing, skipping item: {item}")
            continue

        track_id = track["id"]

        # Skip songs already in CSV or if track_id is None
        if track_id is None or scrap.check_seen_track(track_id, csv):
            print(f"Skipping (id): {track['name']}")
            continue

        print(f"Added (id): {track['name']}")
        track_ids.append(track_id)

    # Fetch audio features in batches of 100 tracks
    for i in range(0, len(track_ids), 100):
        batch_ids = [
            tid for tid in track_ids[i : i + 100] if tid is not None
        ]  # Ensure track IDs are not None
        if not batch_ids:  # Skip empty batches
            continue
        try:
            audio_features = sp.audio_features(batch_ids)
        except SpotifyException as e:
            handle_spotify_exception(e)
            continue

        # Process each track
        for j, track_id in enumerate(batch_ids):
            track_info = next(
                (t for t in all_tracks if t["track"] and t["track"]["id"] == track_id),
                None,
            )

            if track_info is None:
                continue

            track = track_info["track"]
            album = track["album"]
            artists = [
                {"artist_id": artist["id"], "artist_name": artist["name"]}
                for artist in track["artists"]
            ]

            # Combine album, track, and audio features data
            track_data = {
                "album_id": album["id"],
                "release_date": album["release_date"],
                "release_date_precision": album["release_date_precision"],
                "album_restrictions": album.get("restrictions", "none"),
                "track_id": track_id,
                "track_name": track["name"],
                "track_duration_ms": track["duration_ms"],
                "track_explicit": "yes" if track["explicit"] else "no",
                "track_restrictions": track.get("restrictions", "none"),
                "track_popularity": track["popularity"],
                "track_preview_url": track["preview_url"],
            }

            # Add audio features data (if available)
            audio = audio_features[j]
            if audio:
                audio_features_data = {
                    "acousticness": audio["acousticness"],
                    "analysis_url": audio["analysis_url"],
                    "danceability": audio["danceability"],
                    "energy": audio["energy"],
                    "instrumentalness": audio["instrumentalness"],
                    "key": audio["key"],
                    "liveness": audio["liveness"],
                    "loudness": audio["loudness"],
                    "mode": audio["mode"],
                    "speechiness": audio["speechiness"],
                    "tempo": audio["tempo"],
                    "time_signature": audio["time_signature"],
                    "valence": audio["valence"],
                }
            else:
                # If no audio features available, set to None
                audio_features_data = {
                    key: None
                    for key in [
                        "acousticness",
                        "analysis_url",
                        "danceability",
                        "energy",
                        "instrumentalness",
                        "key",
                        "liveness",
                        "loudness",
                        "mode",
                        "speechiness",
                        "tempo",
                        "time_signature",
                        "valence",
                    ]
                }

            combined_data = {**track_data, **audio_features_data, "artists": artists}
            scrap.save_seen_track(combined_data, csv)
            print(f"Added (track): {track['name']}")
        time.sleep(1)

    scrap.save_seen_playlists(playlist_id, "playlists.json")


playlists = scrap.load_queued_playlists("playlists.json")
tracks = scrap.load_seen_track_file("tracks.csv")

print(f"Starting...")

for i, playlist_id in enumerate(playlists):
    print(f"Scraping: {playlist_id} ({i + 1}/{len(playlists)})")

    scrape_playlist(playlist_id, tracks)

    if not i == len(playlists) - 1:
        time.sleep(10)

print("Done.")
scrap.unload_seen_track_file(tracks)
