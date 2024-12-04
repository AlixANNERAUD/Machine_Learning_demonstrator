from rest_framework.decorators import api_view
from django.apps import apps
import pandas
import logging
from django.http import JsonResponse

from . import data

CONFIGURATION = apps.get_app_config("application")
PCA_PATH = f"{CONFIGURATION.data_path}/pca.hdf"

def load_pca(path):
    logging.info("Loading PCA ...")

    embeddings = data.get_embeddings()
    try:
        pca = pandas.read_hdf(path, key="pca")


        if pca.shape[0] != embeddings.shape[0]:
            logging.info("PCA shape does not match, regenerating ...")
            raise FileNotFoundError

        return pca
    except FileNotFoundError:
        logging.info("PCA file not found, generating ...")

        from sklearn.decomposition import PCA

        embeddings = data.get_embeddings()

        pca_model = PCA(n_components=3)

        pca = pca_model.fit_transform(embeddings)

        pca = pandas.DataFrame(pca, columns=["x", "y", "z"])

        pca.to_hdf(path, key="pca")

        logging.info("PCA generated")

        return pca
    except Exception as e:
        logging.error(f"Error loading PCA: {e}")
        raise e

def get_pca():
    global PCA

    if PCA is None:
        PCA = load_pca(PCA_PATH)

    return PCA

PCA = None

@api_view(["GET"])
def pca_view(request):
    pca = get_pca()

    plot_data = {
        "x": pca["x"].to_list(),
        "y": pca["y"].to_list(),
        "z": pca["z"].to_list(),
        "labels": data.get_metadata()["track_name"].to_list(),
    }

    return JsonResponse(plot_data)