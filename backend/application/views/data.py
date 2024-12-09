from django.apps import apps
import logging
import numpy
import pandas
import pickle
import os
from . import deezer

CONFIGURATION = apps.get_app_config("application")

EMBEDDINGS = None
METADATA = None
ALBUMS = None

METADATA_PATH = os.path.join(CONFIGURATION.data_path, "metadata.pickle")
EMBEDDINGS_PATH = os.path.join(CONFIGURATION.data_path, "embeddings.pickle")
ALBUMS_PATH = os.path.join(CONFIGURATION.data_path, "albums.pickle")


def save():
    global EMBEDDINGS, METADATA, ALBUMS

    if EMBEDDINGS is None or METADATA is None or ALBUMS is None:
        raise ValueError("Data not loaded")

    logging.info("Saving data")

    try:
        with open(EMBEDDINGS_PATH, "wb") as file:
            pickle.dump(EMBEDDINGS, file)

        with open(METADATA_PATH, "wb") as file:
            pickle.dump(METADATA, file)

        with open(ALBUMS_PATH, "wb") as file:
            pickle.dump(ALBUMS, file)

    except Exception as e:
        logging.error(f"Error saving data: {e}")
        raise e

def track_exists(track_id):
    global EMBEDDINGS

    return track_id in EMBEDDINGS

def load_data():
    global EMBEDDINGS, METADATA, ALBUMS

    if EMBEDDINGS is not None or METADATA is not None or ALBUMS is not None:
        return

    try:
        with open(EMBEDDINGS_PATH, "rb") as file:
            EMBEDDINGS = pickle.load(file)

        logging.info(f"Loaded {len(EMBEDDINGS)} embeddings")
    except FileNotFoundError:
        logging.info("Embeddings file not found, creating empty data")
        EMBEDDINGS = {}
    except Exception as e:
        logging.error(f"Error loading embeddings: {e}")
        raise e

    try:
        with open(METADATA_PATH, "rb") as file:
            METADATA = pickle.load(file)

        logging.info(f"Loaded {len(METADATA)} metadata")
    except FileNotFoundError:
        logging.info("Metadata file not found, creating empty data")
        METADATA = {}
    except Exception as e:
        logging.error(f"Error loading metadata: {e}")
        raise e

    # Remove metadata for tracks that do not have embeddings
    for track_id in list(METADATA.keys()):
        if track_id not in EMBEDDINGS:
            logging.info(f"Removing metadata for track {track_id}")
            del METADATA[track_id]

    # Get metadata for tracks that do not have metadata
    for track_id in EMBEDDINGS.keys():
        if track_id not in METADATA:
            logging.info(f"Getting metadata for track {track_id}")
            metadata = deezer.get_track(track_id)
            METADATA[track_id] = metadata

    try:
        with open(ALBUMS_PATH, "rb") as file:
            ALBUMS = pickle.load(file)

        logging.info(f"Loaded {len(ALBUMS)} albums")
    except FileNotFoundError:
        logging.info("ALBUMS file not found, creating empty data")
        ALBUMS = {}
    except Exception as e:
        logging.error(f"Error loading ALBUMS: {e}")
        raise e

    # Remove ALBUMS for tracks that do not have metadata
    for track_id in list(ALBUMS.keys()):
        if track_id not in METADATA:
            logging.info(f"Removing album for track {track_id}")
            del ALBUMS[track_id]

    # Get ALBUMS for tracks that do not have ALBUMS
    for track_id, track in METADATA.items():
        if track_id not in ALBUMS:
            logging.info(f"Getting album for track {track_id}")
            album = deezer.get_album(track["album"]["id"])
            ALBUMS[track_id] = album

    save()

load_data()

def get_albums(album_id):
    global ALBUMS

    return ALBUMS[album_id]


def get_embeddings():
    global EMBEDDINGS

    return EMBEDDINGS


def get_metadata():
    global METADATA

    return METADATA


def get_track(track_id):
    global EMBEDDINGS, METADATA

    metadata = METADATA[track_id]
    embedding = EMBEDDINGS[track_id]

    return metadata, embedding

def add_track(track_id, embedding, metadata):
    global EMBEDDINGS, METADATA

    if track_id in EMBEDDINGS:
        raise ValueError(f"Track {track_id} already exists")

    EMBEDDINGS[track_id] = embedding
    METADATA[track_id] = metadata

def add_album(album_id, album):
    global ALBUMS

    if album_id in ALBUMS:
        raise ValueError(f"Album {album_id} already exists")

    ALBUMS[album_id] = album