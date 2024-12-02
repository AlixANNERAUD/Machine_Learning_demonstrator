import json

import pandas as pd

file_path = "./tracks.csv"
raw_tracks = pd.read_csv(file_path)

tracks = raw_tracks[
    [
        # Metadata
        "release_date",
        "release_date_precision",  # Will be removed
        "track_duration_ms",
        "track_explicit",  # Ignored
        # Audio features
        "acousticness",
        "danceability",
        "energy",
        "instrumentalness",
        "liveness",
        "loudness",
        "mode",  # Ignored
        "speechiness",
        "tempo",
        "time_signature",  # Ignored
        "valence",
    ]
]

# Embed the data


def convert_date_with_precision(date):
    """Convert %Y-%m-%D or %Y-%m or %Y to a year"""

    return int(date.split("-")[0])


# Apply the conversion to the dataframe
tracks["timestamp"] = tracks.apply(
    lambda row: convert_date_with_precision(row["release_date"]),
    axis=1,
)

tracks = tracks.dropna()
tracks = tracks[tracks["track_duration_ms"] > 0]  # Some tracks have a duration of 0
tracks = tracks[tracks["timestamp"] > 0]  # Some tracks have 0000 as date

tracks = tracks.drop(
    columns=[
        "release_date",  # timestamp
        "release_date_precision",  # timestamp
        "mode",
        "time_signature",
        "track_explicit",
    ]
)

print(tracks.info())

import numpy as np
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
tracks_scaled = scaler.fit_transform(tracks)


def get_nearest_tracks(tracks_scaled, track_id, n=5, artists=False):
    track_index = np.where(raw_tracks["track_id"] == track_id)[0][0]
    track = tracks_scaled[track_index]

    distances = np.linalg.norm(tracks_scaled - track, axis=1)

    # 5 closest tracks excluding the track itself (index 0)
    closest_tracks = raw_tracks.iloc[np.argsort(distances)[1 : n + 1]]

    if artists:
        closest_tracks.loc[:, "artists"] = closest_tracks.loc[:, "artists"].apply(
            lambda artists: json.loads(artists.replace("'", '"'))[0]["artist_name"]
        )

        return closest_tracks[["track_name", "track_id", "artists"]]

    return closest_tracks[["track_name", "track_id"]]


track_id = "2VxeLyX666F8uXCJ0dZF8B"  # Lady Gaga - Shallow
print(get_nearest_tracks(tracks_scaled, track_id, 5, artists=True))


import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
tracks_pca = pca.fit_transform(tracks_scaled)

# All tracks
plt.scatter(
    tracks_pca[:, 0],
    tracks_pca[:, 1],
    c=tracks["timestamp"],
    alpha=0.5,
    s=2,
)
plt.colorbar()

# Closest tracks
closest_tracks = get_nearest_tracks(tracks_scaled, track_id, 5)
closest_tracks_pca = pca.transform(
    tracks_scaled[np.where(raw_tracks["track_id"].isin(closest_tracks["track_id"]))]
)
plt.scatter(
    closest_tracks_pca[:, 0],
    closest_tracks_pca[:, 1],
    c="red",
    alpha=0.5,
    s=2,
    label="Closest tracks",
)

# Selected track
track_index = np.where(raw_tracks["track_id"] == track_id)[0][0]
track_pca = tracks_pca[track_index]
plt.scatter(track_pca[0], track_pca[1], c="black", s=5, label="Selected track")

plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.title("PCA of tracks")
plt.show()
