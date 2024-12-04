from django.apps import apps
import logging
import numpy
import pandas

CONFIGURATION = apps.get_app_config("application")

DATA = None
EMBEDDINGS_PATH = f"{CONFIGURATION.data_path}/embeddings_330.npy"
IDENTIFIERS_PATH = f"{CONFIGURATION.data_path}/id_embeddings_330.npy"
METADATA_PATH = f"{CONFIGURATION.data_path}/tracks.hdf"


def load_data():
    try:
        embeddings = numpy.load(EMBEDDINGS_PATH)
        id = numpy.load(IDENTIFIERS_PATH)
        metadata = pandas.read_hdf(METADATA_PATH, key="metadata")
        
        metadata.dropna(inplace=True)

        if metadata.shape[0] != embeddings.shape[0] != id.shape[0]:
            logging.warning("Metadata, embeddings and identifiers do not match")

    except FileNotFoundError:
        logging.info("Embeddings file not found, creating empty data")

        embeddings = numpy.zeros(0)
        id = numpy.zeros(0)
        metadata = pandas.DataFrame()

    except Exception as e:
        logging.error(f"Error loading embeddings: {e}")
        raise e

    return {"embeddings": embeddings, "identifiers": id, "metadata": metadata}


def get_embeddings():
    global DATA

    if DATA is None:
        DATA = load_data()

    return DATA["embeddings"]


def get_identifiers():
    global DATA

    if DATA is None:
        DATA = load_data()

    return DATA["identifiers"]


def get_metadata():
    global DATA

    if DATA is None:
        DATA = load_data()

    return DATA["metadata"]


def get_embedding(track_id):
    embeddings = get_embeddings()
    identifiers = get_identifiers()

    index = numpy.where(identifiers == track_id)

    if len(index[0]) == 0:
        return None

    return embeddings[index[0][0]]


def add_track(track_id, embedding, metadata):
    global DATA

    if DATA is None:
        DATA = load_data()

    DATA["embeddings"] = numpy.append(DATA["embeddings"], [embedding], axis=0)
    DATA["identifiers"] = numpy.append(DATA["identifiers"], [track_id], axis=0)
    DATA["metadata"] = DATA["metadata"].append(metadata, ignore_index=True)

    numpy.save(f"{CONFIGURATION.data_path}/embeddings_330.npy", DATA["embeddings"])
    numpy.save(f"{CONFIGURATION.data_path}/id_embeddings_330.npy", DATA["identifiers"])
    DATA["metadata"].to_hdf(METADATA_PATH, key="metadata")


    return True
