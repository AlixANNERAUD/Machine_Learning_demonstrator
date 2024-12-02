from rest_framework.decorators import api_view
from django.apps import apps
import pandas
import logging
from django.http import JsonResponse

from . import tracks

configuration = apps.get_app_config("application")


def load_umap(tracks: pandas.DataFrame, path: str):
    logging.info("Loading UMAP ...")

    try:
        umap = pandas.read_hdf(path, key="umap")

        if umap.shape[0] != tracks.shape[0]:
            logging.info("UMAP shape does not match, regenerating ...")
            raise FileNotFoundError

        return umap
    except FileNotFoundError:
        logging.info("UMAP file not found, generating ...")

        import umap

        numeric_columns = tracks.select_dtypes(include=["float64", "int64"]).dropna(
            axis=0
        )

        umap_model = umap.UMAP(
            n_components=3, n_neighbors=10, min_dist=0.1, metric="correlation"
        )

        umap = umap_model.fit_transform(numeric_columns)

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
        UMAP = load_umap(tracks.get_tracks(), f"{configuration.data_path}/umap.hdf")

    return UMAP

UMAP = None

@api_view(["GET"])
def umap_view(request):
    umap = get_umap()

    data = {
        "x": umap["x"].to_list(),
        "y": umap["y"].to_list(),
        "z": umap["z"].to_list(),
        "labels": tracks.get_tracks()["track_name"].to_list(),
    }

    return JsonResponse(data)
