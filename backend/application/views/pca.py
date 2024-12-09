from rest_framework.decorators import api_view
from django.apps import apps
import logging
from django.http import JsonResponse
import numpy
import pickle

from . import data

CONFIGURATION = apps.get_app_config("application")
PCA_PATH = f"{CONFIGURATION.data_path}/PCA.pickle"

PCA = None


def generate_PCA():
    from sklearn.decomposition import PCA

    # Create a list of labels (artist - title)
    embeddings = data.get_embeddings()
    metadata = data.get_metadata()
    labels = []
    for track_id in embeddings.keys():
        track_metadata = metadata[track_id]

        labels.append(
            f"{track_metadata['artist']['name']} - {track_metadata['title_short']}"
        )

    # Create a PCA model
    pca_model = PCA(n_components=3)
    embeddings_values = numpy.array(list(embeddings.values()))
    pca = pca_model.fit_transform(embeddings_values)

    return {
        "x": pca[:, 0].tolist(),
        "y": pca[:, 1].tolist(),
        "z": pca[:, 2].tolist(),
        "labels": labels,
    }


def load_PCA():
    global PCA, PCA_PATH

    embeddings = data.get_embeddings()

    if PCA is not None and len(PCA["labels"]) == len(embeddings):
        return

    logging.info("Loading PCA ...")

    try:
        # Load the PCA from a file
        with open(PCA_PATH, "rb") as file:
            PCA = pickle.load(file)

        if len(PCA["labels"]) != len(embeddings):
            logging.info("PCA shape does not match, regenerating ...")
            raise FileNotFoundError

    except FileNotFoundError:
        logging.info("PCA file not found, generating ...")

        PCA = generate_PCA()

        # Save the generated PCA to a file
        with open(PCA_PATH, "wb") as file:
            pickle.dump(PCA, file)

        logging.info("PCA generated")

    except Exception as e:
        logging.error(f"Error loading PCA: {e}")
        raise e


@api_view(["GET"])
def pca_view(request):
    global PCA

    load_PCA()

    return JsonResponse(PCA)
