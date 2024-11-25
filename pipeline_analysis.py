import csv

import numpy as np

from modules.conversions import get_artist_string

datasetname = "tracks.csv"
filename = "embeddings_330.npy"
filename_id = f"id_{filename}"

# Load the dataset and print the shape
f = open(datasetname, "r")
dataset = csv.DictReader(f)
embeddings = np.load(filename)
id_embeddings = np.load(filename_id)

print(f"Embeddings shape: {embeddings.shape}")
# Shape (N, 768) where N is the number of embeddings
# exit()

"""
We want to find the K nearest neighbors of a given embedding (by id).
"""

# Define the embedding and the number of neighbors
target_id = "7oaEjLP2dTJLJsITbAxTOz"

idx = np.where(id_embeddings == target_id)
if len(idx[0]) == 0:
    print(f"[Warning] ID {target_id} not found in the dataset.")
    exit()
embedding = embeddings[idx[0][0]]
K = 5

# # Compute the cosine similarity between the embedding and all the embeddings
cosine_similarities = np.dot(embeddings, embedding) / (
    np.linalg.norm(embeddings, axis=1) * np.linalg.norm(embedding)
)

# Get the indices of the K most similar embeddings
nearest_indices = np.argsort(cosine_similarities)[::-1][1 : K + 1]

# Get the IDs of the nearest embeddings
nearest_ids = id_embeddings[nearest_indices]

# print(f"Nearest IDs: {nearest_ids}")
# print(f"Nearest cosine similarities: {cosine_similarities[nearest_indices]}")

tracks = np.empty((6,), dtype=object)
for row in dataset:
    if row["track_id"] in nearest_ids:
        tracks[np.where(nearest_ids == row["track_id"])[0][0] + 1] = row
    elif row["track_id"] == target_id:
        tracks[0] = row

print("-" * 64)
for i, track in enumerate(tracks):
    if i == 1:
        print("|" + "-" * 63)
    print(
        f"| {track['track_name']} by {get_artist_string(track['artists'])} ({i== 0 and 1 or cosine_similarities[nearest_indices[i-1]]:.2f})"
    )
print("-" * 64)

f.close()


f = open(datasetname, "r")
dataset = csv.DictReader(f)

from sklearn.decomposition import PCA

# Perform PCA on the embeddings
pca = PCA()
pca.fit(embeddings)
pca_embeddings = pca.transform(embeddings)

# Get the PCA coordinates of the target embedding
pca_embedding = pca_embeddings[np.where(id_embeddings == target_id)[0][0]]

# Get the PCA coordinates of the nearest embeddings
pca_nearest_embeddings = pca_embeddings[nearest_indices]

# Find the number of components that explain 95% of the variance
explained_variance_ratio = pca.explained_variance_ratio_
cumulative_variance_ratio = np.cumsum(explained_variance_ratio)
n_components = np.argmax(cumulative_variance_ratio > 0.99) + 1

# import matplotlib.pyplot as plt

# plt.plot(cumulative_variance_ratio)
# plt.axvline(n_components, color="red", linestyle="--")
# plt.xlabel("Number of components")
# plt.ylabel("Cumulative explained variance")
# plt.title("PCA explained variance")
# plt.show()
# print(f"Number of components: {n_components}")

# Compute the cosine similarity between the PCA embedding and all the PCA embeddings
cosine_similarities_pca = np.dot(pca_embeddings, pca_embedding) / (
    np.linalg.norm(pca_embeddings, axis=1) * np.linalg.norm(pca_embedding)
)

# Get the indices of the K most similar PCA embeddings
nearest_indices_pca = np.argsort(cosine_similarities_pca)[::-1][1 : K + 1]

# Get the IDs of the nearest PCA embeddings
nearest_ids_pca = id_embeddings[nearest_indices_pca]

# Print the nearest tracks using PCA embeddings
tracks_pca = np.empty((6,), dtype=object)
for row in dataset:
    if row["track_id"] in nearest_ids_pca:
        tracks_pca[np.where(nearest_ids_pca == row["track_id"])[0][0] + 1] = row
    elif row["track_id"] == target_id:
        tracks_pca[0] = row

print("-" * 64)
for i, track in enumerate(tracks_pca):
    if i == 1:
        print("|" + "-" * 63)
    print(
        f"| {track['track_name']} by {get_artist_string(track['artists'])} ({i== 0 and 1 or cosine_similarities_pca[nearest_indices_pca[i-1]]:.2f})"
    )
print("-" * 64)

f.close()
