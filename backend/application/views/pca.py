from rest_framework.decorators import api_view
from django.apps import apps
import logging
from django.http import JsonResponse
import numpy
import pickle

from . import data

CONFIGURATION = apps.get_app_config("application")
PCA_PATH = f"{CONFIGURATION.data_path}/PCA.pickle"
EXPLAINED_VARIANCE_RATIO_PATH = (
    f"{CONFIGURATION.data_path}/explained_variance_ratio.pickle"
)

PCA = None
EXPLAINED_VARIANCE_RATIO = None


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

    # Compute the explained variance ratio
    explained_variance_ratio = pca_model.explained_variance_ratio_

    return {
        "x": pca[:, 0].tolist(),
        "y": pca[:, 1].tolist(),
        "z": pca[:, 2].tolist(),
        "labels": labels,
    }, explained_variance_ratio.tolist()


def load_PCA():
    global PCA, PCA_PATH, EXPLAINED_VARIANCE_RATIO, EXPLAINED_VARIANCE_RATIO_PATH

    embeddings = data.get_embeddings()

    if PCA is not None and len(PCA["labels"]) == len(embeddings):
        return

    logging.info("Loading PCA ...")

    try:
        # Load the PCA from a file
        with open(PCA_PATH, "rb") as file:
            PCA = pickle.load(file)

        # Load the explained variance ratio from a file
        with open(EXPLAINED_VARIANCE_RATIO_PATH, "rb") as file:
            EXPLAINED_VARIANCE_RATIO = pickle.load(file)

        if len(PCA["labels"]) != len(embeddings):
            logging.info("PCA shape does not match, regenerating ...")
            raise FileNotFoundError

    except FileNotFoundError:
        logging.info("PCA file not found, generating ...")

        PCA, EXPLAINED_VARIANCE_RATIO = generate_PCA()

        # Save the generated PCA to a file
        with open(PCA_PATH, "wb") as file:
            pickle.dump(PCA, file)

        # Save the generated explained variance ratio to a file
        with open(EXPLAINED_VARIANCE_RATIO_PATH, "wb") as file:
            pickle.dump(EXPLAINED_VARIANCE_RATIO, file)

        logging.info("PCA generated")

    except Exception as e:
        logging.error(f"Error loading PCA: {e}")
        raise e


@api_view(["GET"])
def pca_view(request):
    global PCA

    load_PCA()

    return JsonResponse(PCA)


@api_view(["GET"])
def explained_variance_ratio_view(request):
    global EXPLAINED_VARIANCE_RATIO

    load_PCA()

    return JsonResponse({"explained_variance_ratio": EXPLAINED_VARIANCE_RATIO})
