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

# For now, we will drop categorical features
tracks = tracks.drop(
    columns=[
        "release_date",  # We have the timestamp
        "release_date_precision",  # We have the timestamp
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


def get_nearest_tracks(tracks_scaled, track_id, n=5):
    track_index = np.where(raw_tracks["track_id"] == track_id)[0][0]
    track = tracks_scaled[track_index]

    distances = np.linalg.norm(tracks_scaled - track, axis=1)

    # 5 closest tracks excluding the track itself (index 0)
    closest_tracks = raw_tracks.iloc[np.argsort(distances)[1 : n + 1]]

    return closest_tracks[["track_name", "track_id"]]


track_id = "4vO24keemHgi3JoCLIQAq9"
print(get_nearest_tracks(tracks_scaled, track_id, 5))


# PCA
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
tracks_pca = pca.fit_transform(tracks_scaled)

# Plot the PCA, color by year
import matplotlib.pyplot as plt

plt.scatter(tracks_pca[:, 0], tracks_pca[:, 1], c=tracks["timestamp"], alpha=0.5, s=2)
# Get the ids of the 5 closest tracks
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
plt.xlabel("PCA 1")
plt.ylabel("PCA 2")
plt.title("PCA of tracks")

plt.colorbar()
plt.show()
