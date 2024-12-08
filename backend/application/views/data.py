from django.apps import apps
import logging
import numpy
import pandas
import pickle

CONFIGURATION = apps.get_app_config("application")

DATA = None
TRACKS_PATH = os.path.join(CONFIGURATION.data_path, "tracks.pickle")

def load_data():
    try:
        with open(TRACKS_PATH, "rb") as file:
            DATA = pickle.load(file)
            

    except FileNotFoundError:
        logging.info("Embeddings file not found, creating empty data")

        DATA = {}

    except Exception as e:
        logging.error(f"Error loading embeddings: {e}")
        raise e

    return {"embeddings": embeddings, "metadata": metadata}


def get_embeddings():
    global DATA

    if DATA is None:
        DATA = load_data()
    
    # From dict to numpy array
    embeddings = numpy.array(list(DATA["embeddings"].items()))
    
    return embeddings


def get_identifiers():
    global DATA

    if DATA is None:
        DATA = load_data()
        
    # From dict to numpy array
    identifiers = numpy.array(list(DATA["embeddings"].keys()))

    return DATA["identifiers"]


def get_track(track_id):
    global DATA

    if DATA is None:
        DATA = load_data()

    metadata = DATA["metadata"][track_id]
    embedding = DATA["embeddings"][track_id]

    return metadata, embedding


def add_track(track_id, embedding, metadata):
    global DATA

    if DATA is None:
        DATA = load_data()

    if track_id in DATA["embeddings"] or track_id in DATA["metadata"]:
        raise ValueError(f"Track {track_id} already exists")
    
    DATA["embeddings"][track_id] = embedding
    DATA["identifiers"][track_id] = track_id
    

def save_data():
    global DATA

    if DATA is None:
        return

    try:
        with open(EMBEDDINGS_PATH, "wb") as file:
            pickle.dump(DATA["embeddings"], file)
        
        with open(METADATA_PATH, "wb") as file:
            pickle.dump(DATA["metadata"], file)
            
    except Exception as e:
        logging.error(f"Error saving data: {e}")
        raise e
