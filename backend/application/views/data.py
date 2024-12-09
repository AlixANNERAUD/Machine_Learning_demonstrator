from django.apps import apps
import logging
import numpy
import pandas
import pickle
import os

CONFIGURATION = apps.get_app_config("application")

EMBEDDINGS = None
METADATA = None

METADATA_PATH = os.path.join(CONFIGURATION.data_path, "metadata.pickle")
EMBEDDINGS_PATH = os.path.join(CONFIGURATION.data_path, "embeddings.pickle")


def load_data():
    global EMBEDDINGS, METADATA, METADATA_PATH, EMBEDDINGS_PATH

    if EMBEDDINGS is not None or METADATA is not None:
        return

    try:
        with open(METADATA_PATH, "rb") as file:
            METADATA = pickle.load(file)

        with open(EMBEDDINGS_PATH, "rb") as file:
            EMBEDDINGS = pickle.load(file)

        if len(EMBEDDINGS) != len(METADATA):
            raise ValueError("Metadata and embeddings do not match")

        logging.info(f"Loaded {len(EMBEDDINGS)} embeddings")

    except FileNotFoundError:
        logging.info("Embeddings file not found, creating empty data")

        EMBEDDINGS = {}
        METADATA = {}

    except Exception as e:
        logging.error(f"Error loading embeddings: {e}")
        raise e


load_data()


def get_embeddings():
    global EMBEDDINGS

    return EMBEDDINGS

def get_metadata():
    global METADATA

    return METADATA

def get_track(track_id):
    global EMDEDINGS, METADATA

    metadata = METADATA[track_id]
    embedding = EMDEDINGS[track_id]

    return metadata, embedding


def add_track(track_id, embedding, metadata):
    global EMBEDDINGS, METADATA

    if track_id in EMBEDDINGS or track_id in METADATA:
        raise ValueError(f"Track {track_id} already exists")

    EMBEDDINGS[track_id] = embedding
    METADATA[track_id] = metadata


def save():
    global EMBEDDINGS, METADATA

    try:
        with open(EMBEDDINGS_PATH, "wb") as file:
            pickle.dump(EMBEDDINGS, file)

        with open(METADATA_PATH, "wb") as file:
            pickle.dump(METADATA, file)

    except Exception as e:
        logging.error(f"Error saving data: {e}")
        raise e
