from rest_framework.decorators import api_view
from django.apps import apps
import pandas
import logging
from django.http import JsonResponse

from . import tracks

configuration = apps.get_app_config("application")


def load_pca(tracks, path):
    logging.info("Loading PCA ...")

    try:
        pca = pandas.read_hdf(path, key="pca")

        if pca.shape[0] != tracks.shape[0]:
            logging.info("PCA shape does not match, regenerating ...")
            raise FileNotFoundError

        return pca
    except FileNotFoundError:
        logging.info("PCA file not found, generating ...")

        from sklearn.decomposition import PCA

        numeric_columns = tracks.select_dtypes(include=["float64", "int64"]).dropna(
            axis=0
        )

        pca_model = PCA(n_components=3)

        pca = pca_model.fit_transform(numeric_columns)

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
        PCA = load_pca(tracks.get_tracks(), f"{configuration.data_path}/pca.hdf")

    return PCA

PCA = None

@api_view(["GET"])
def pca_view(request):
    pca = get_pca()

    data = {
        "x": pca["x"].to_list(),
        "y": pca["y"].to_list(),
        "z": pca["z"].to_list(),
        "labels": tracks.get_tracks()["track_name"].to_list(),
    }

    return JsonResponse(data)