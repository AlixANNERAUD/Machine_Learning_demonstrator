import json
import torch
from transformers import AutoTokenizer, AutoModel
import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


# Charger le modèle et le tokenizer
# bert-base-cased
MODEL_NAME = "bert-base-multilingual-uncased"
device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModel.from_pretrained(MODEL_NAME).to(device)

# Fonction pour préparer le texte
def prepare_text(text):
    inputs = tokenizer(text=text, return_tensors="pt", padding=True, truncation=True, max_length=512)
    return inputs

# Fonction pour extraire l'embedding d'une chanson
def extract_text_embedding(text, model, tokenizer):
    inputs = prepare_text(text)
    inputs = {key: val.to(model.device) for key, val in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
    
    # Utiliser mean pooling sur les tokens pour créer un vecteur unique
    hidden_states = outputs.last_hidden_state
    text_embedding = hidden_states.mean(dim=1)
    # Autre options : hidden_states[:, 0, :] pour le premier token (CLS), ou pour le max pooling : hidden_states.max(dim=1)
    
    return text_embedding.cpu().numpy()

# Charger le dataset JSON
def load_dataset(json_path):
    with open(json_path, "r") as f:
        data = json.load(f)
    return data

# Fonction principale pour extraire tous les embeddings
def extract_embeddings_from_dataset(dataset_path):
    # Charger les données
    data = load_dataset(dataset_path)

    embeddings = []
    ids = []

    # Itérer sur chaque chanson du dataset
    for song in data:
        song_id = song["id_song"]
        lyrics = song["lyrics"]

        if not lyrics:
            print(f"Skipping song with ID {song_id} due to null or empty lyrics.")
            continue

        # Extraire l'embedding pour les paroles
        embedding = extract_text_embedding(lyrics, model, tokenizer)
        embeddings.append(embedding)
        ids.append(song_id)

    # Convertir les embeddings en une matrice numpy
    embeddings = np.vstack(embeddings)

    return ids, embeddings

# Fonction pour appliquer PCA
def apply_pca(embeddings, n_components=3):
    """
    Réduit la dimension des embeddings à n_components en utilisant PCA.

    Args:
        embeddings (numpy.ndarray): Matrice des embeddings.
        n_components (int): Nombre de dimensions cible (par défaut : 3).

    Returns:
        numpy.ndarray: Embeddings réduits à n_components dimensions.
    """
    pca = PCA(n_components=n_components)
    reduced_embeddings = pca.fit_transform(embeddings)
    return reduced_embeddings

# Fonction pour appliquer t-SNE
def apply_tsne(embeddings, n_components=3, perplexity=30, random_state=42):
    """
    Réduit la dimension des embeddings à n_components en utilisant t-SNE.

    Args:
        embeddings (numpy.ndarray): Matrice des embeddings.
        n_components (int): Nombre de dimensions cible (par défaut : 3).
        perplexity (float): Paramètre de t-SNE pour contrôler la densité des voisins (par défaut : 30).
        random_state (int): Graine aléatoire pour reproduire les résultats.

    Returns:
        numpy.ndarray: Embeddings réduits à n_components dimensions.
    """
    tsne = TSNE(n_components=n_components, perplexity=perplexity, random_state=random_state)
    reduced_embeddings = tsne.fit_transform(embeddings)
    return reduced_embeddings

# Modification du plot pour utiliser une méthode configurable
def plot_embeddings_3d(embeddings_3d, method="PCA"):
    """
    Visualise les embeddings en 3D.

    Args:
        embeddings_3d (numpy.ndarray): Embeddings réduits à 3 dimensions.
        method (str): Méthode utilisée pour la réduction (PCA ou t-SNE).
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Tracer les points 3D
    ax.scatter(embeddings_3d[:, 0], embeddings_3d[:, 1], embeddings_3d[:, 2], c='blue', marker='o')

    # Ajouter des labels et un titre
    ax.set_xlabel('Composante 1')
    ax.set_ylabel('Composante 2')
    ax.set_zlabel('Composante 3')
    ax.set_title(f'Représentation 3D des embeddings ({method})')

    # Afficher la figure
    plt.show()

def save_embeddings_to_json(ids, embeddings, output_path="saved_embeddings.json"):
    """
    Enregistre les embeddings dans un fichier JSON.

    Args:
        ids (list): Liste des IDs des chansons.
        embeddings (numpy.ndarray): Matrice des embeddings.
        output_path (str): Chemin du fichier de sortie (par défaut : "saved_embeddings.json").
    """
    embeddings_list = embeddings.tolist()  # Convertir les embeddings en liste pour JSON

    data_to_save = [{"id_song": song_id, "embedding": embedding} for song_id, embedding in zip(ids, embeddings_list)]

    with open(output_path, "w") as f:
        json.dump(data_to_save, f, indent=4)


def get_cosine_similarity(embeddings, embedding, results=5):
    # Calculate the cosine similarity between the embeddings
    cosine_similarities = np.dot(embeddings, embedding) / (
        np.linalg.norm(embeddings, axis=1) * np.linalg.norm(embedding)
    )

    # Get the nearest indices
    nearest_indices = np.argsort(cosine_similarities)[::-1][1:results]

    return nearest_indices

def get_similar_tracks(embedding, results=5, file_path="saved_embeddings.json"):
    with open(file_path, "r") as f:
        data = json.load(f)

    identifiers = []
    embeddings = []

    for item in data:
        identifiers.append(item["id_song"])
        embeddings.append(item["embedding"])

    embeddings = np.array(embeddings)

    nearest_indices = get_cosine_similarity(
        embeddings, embedding, results=results
    )

    return [identifiers[i] for i in nearest_indices]

def get_embedding_by_id(song_id, file_path="saved_embeddings.json"):
    """
    Récupère l'embedding d'une chanson à partir de son ID.

    Args:
        song_id (str): ID de la chanson.
        file_path (str): Chemin du fichier JSON contenant les embeddings (par défaut : "saved_embeddings.json").

    Returns:
        numpy.ndarray: Embedding de la chanson si trouvé, sinon None.
    """
    with open(file_path, "r") as f:
        data = json.load(f)

    for item in data:
        if item["id_song"] == song_id:
            return np.array(item["embedding"])

    print(f"Embedding for song ID {song_id} not found.")
    return None

# Exemple d'utilisation
# dataset_path = "./lyrics.json"  # Chemin vers votre fichier JSON
# ids, embeddings = extract_embeddings_from_dataset(dataset_path)

# print("Nombre d'ids extraits :", len(ids))
# print("Dimension des embeddings :", embeddings.shape)

# # Enregistrement des embeddings dans un fichier JSON
# save_embeddings_to_json(ids, embeddings)

# # Choix de la méthode de réduction
# method = "PCA"  # "PCA" ou "t-SNE"

# if method == "PCA":
#     embeddings_3d = apply_pca(embeddings, n_components=3)
# elif method == "t-SNE":
#     embeddings_3d = apply_tsne(embeddings, n_components=3, perplexity=30)

# # Visualiser les embeddings
# plot_embeddings_3d(embeddings_3d, method=method)

id_teste = "36OkygdRZI6Nhspmuzkpn9"
emb = get_embedding_by_id(id_teste)
print(f"{id_teste = }")
print(get_similar_tracks(emb))