from rest_framework.decorators import api_view
from django.apps import apps
import logging
from django.http import JsonResponse
import os
import pickle
import numpy

from . import data

CONFIGURATION = apps.get_app_config("application")
UMAP_PATH = f"{CONFIGURATION.data_path}/UMAP.pickle"

UMAP = None

def load_umap():
    global UMAP, UMAP_PATH

    if UMAP is not None:
        return
    
    logging.info("Loading UMAP ...")

    embeddings = data.get_embeddings()

    try:
        with open(UMAP_PATH, "rb") as file:
            UMAP = pickle.load(file)

        if len(UMAP["labels"]) != len(embeddings):
            logging.info("UMAP shape does not match, regenerating ...")
            raise FileNotFoundError

    except FileNotFoundError:
        logging.info("UMAP file not found, generating ...")

        import umap

        # Create a list of labels (artist - title)
        metadata = data.get_metadata()
        labels = []
        for track_id in embeddings.keys():
            track_metadata = metadata[track_id]

            labels.append(
                f"{track_metadata['artist']['name']} - {track_metadata['title_short']}"
            )
            
        # Create a UMAP model
        umap_model = umap.UMAP(
            n_components=3, n_neighbors=10, min_dist=0.1, metric="correlation"
        )
        embeddings_values = numpy.array(list(embeddings.values()))
        umap = umap_model.fit_transform(embeddings_values)


        UMAP = {
            "x": umap[:, 0].tolist(),
            "y": umap[:, 1].tolist(),
            "z": umap[:, 2].tolist(),
            "labels": labels,
        }
        
        # Save the UMAP to a file
        with open(UMAP_PATH, "wb") as file:
            pickle.dump(UMAP, file)

        logging.info("UMAP generated")

    except Exception as e:
        logging.error(f"Error loading UMAP: {e}")
        raise e

@api_view(["GET"])
def umap_view(request):
    global UMAP
    
    load_umap()

    return JsonResponse(UMAP)
