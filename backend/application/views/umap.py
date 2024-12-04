from rest_framework.decorators import api_view
from django.apps import apps
import pandas
import logging
from django.http import JsonResponse

from . import data

CONFIGURATION = apps.get_app_config("application")
UMAP_PATH = f"{CONFIGURATION.data_path}/umap.hdf"

def load_umap(path: str):
    logging.info("Loading UMAP ...")

    embeddings = data.get_embeddings()

    try:
        umap = pandas.read_hdf(path, key="umap")

        if umap.shape[0] != embeddings.shape[0]:
            logging.info("UMAP shape does not match, regenerating ...")
            raise FileNotFoundError

        return umap
    except FileNotFoundError:
        logging.info("UMAP file not found, generating ...")

        import umap

        umap_model = umap.UMAP(
            n_components=3, n_neighbors=10, min_dist=0.1, metric="correlation"
        )

        umap = umap_model.fit_transform(embeddings)

        umap = pandas.DataFrame(umap, columns=["x", "y", "z"])

        umap.to_hdf(path, key="umap")

        logging.info("UMAP generated")

        return umap
    except Exception as e:
        logging.error(f"Error loading UMAP: {e}")
        raise e

def get_umap():
    global UMAP

    if UMAP is None:
        UMAP = load_umap(UMAP_PATH)

    return UMAP

UMAP = None

@api_view(["GET"])
def umap_view(request):
    umap = get_umap()

    plot_data = {
        "x": umap["x"].to_list(),
        "y": umap["y"].to_list(),
        "z": umap["z"].to_list(),
        "labels": data.get_metadata()["track_name"].to_list(),
    }

    return JsonResponse(plot_data)
