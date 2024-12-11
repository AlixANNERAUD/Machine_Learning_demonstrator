import json
import logging
import os
import pickle

import numpy
from django.apps import apps
from django.http import JsonResponse
from rest_framework.decorators import api_view

from . import data, deezer, processing

CONFIGURATION = apps.get_app_config("application")

BINARIZER = None
MODEL = None

BINARIZER_PATH = os.path.join(CONFIGURATION.data_path, "genre_binarizer.pickle")
MODEL_PATH = os.path.join(CONFIGURATION.data_path, "genre_model.pickle")

HYPERPARAMETERS = {}
SPLITS = 5


def predict_track(embedding):
    global MODEL, BINARIZER

    raw_predictions = MODEL.predict(embedding)

    predictions = list(BINARIZER.inverse_transform(raw_predictions))

    predictions = [int(genre) for genre in predictions[0]]

    return list(predictions)


def train_model():
    from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
    from sklearn.model_selection import GridSearchCV
    from sklearn.multioutput import MultiOutputClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import MultiLabelBinarizer

    logging.info("Training model")

    # Prepare the data for training
    albums = data.get_albums()

    albums_genres = {}
    for identifier, album in albums.items():
        try:
            album_genres = [genre["id"] for genre in album["genres"]["data"]]

            albums_genres[identifier] = album_genres
        except KeyError:
            logging.error(f"Album {identifier} has no genres")

    tracks = data.get_metadata()

    tracks_genres = []
    for track in tracks.values():
        try:
            album_genres = albums_genres[track["album"]["id"]]

            tracks_genres.append(album_genres)
        except KeyError:
            logging.error(f"Track {track['id']} has no album")

    # Binarize the genres
    binarizer = MultiLabelBinarizer()
    tracks_genres = binarizer.fit_transform(tracks_genres)

    # Print the number of tracks by genre
    genres_counts = numpy.sum(tracks_genres, axis=0)

    for genre, count in zip(binarizer.classes_, genres_counts):
        logging.info(f"Genre {genre}: {count} tracks")

    # Get the embeddings
    embeddings = data.get_embeddings()
    embeddings = numpy.array(list(embeddings.values()))

    if len(embeddings) < SPLITS:
        logging.error("Not enough embeddings to train the model")
        logging.warning("Please add more tracks to the database")
        return None, None

    # Get the embeddings
    classifier = MultiOutputClassifier(HistGradientBoostingClassifier())

    # Perform a grid search to find the best hyperparameters
    grid_search = GridSearchCV(
        classifier, HYPERPARAMETERS, cv=SPLITS, n_jobs=-1, scoring="f1_micro"
    )

    grid_search.fit(embeddings, tracks_genres)

    logging.info(f"Gird search best score: {grid_search.best_score_}")

    # Return the best estimator
    return grid_search.best_estimator_, binarizer


def load_model():
    global MODEL, BINARIZER

    # Check if the model is already loaded
    if MODEL is not None and BINARIZER is not None:
        return

    # Try load the model from the file
    try:
        with open(MODEL_PATH, "rb") as file:
            MODEL = pickle.load(file)
            logging.info("Loaded classifier")

        with open(BINARIZER_PATH, "rb") as file:
            BINARIZER = pickle.load(file)
            logging.info("Loaded binarizer")

        logging.info("Loaded model")
    # If the file is not found, train the model
    except FileNotFoundError:
        logging.info("Model file not found, training model")

        MODEL, BINARIZER = train_model()
        if MODEL is None or BINARIZER is None:
            raise ValueError("Model could not be trained")

        with open(MODEL_PATH, "wb") as file:
            pickle.dump(MODEL, file)

        with open(BINARIZER_PATH, "wb") as file:
            pickle.dump(BINARIZER, file)

    except Exception as e:
        logging.error(f"Error loading model: {e}")
        raise e


load_model()


@api_view(["GET"])
def classify_view(request):
    # Get the track id from the request
    track_id = request.GET.get("track_id", "")

    # Check if the track_id is empty
    if track_id == "":
        return JsonResponse({"error": "No track specified"}, status=400)

    # Try to get the embedding from the data
    try:
        _, embedding = data.get_track(track_id)
    # If the embedding is not found, download the track, create the embedding and add it to the data
    except KeyError:
        metadata = deezer.get_track(track_id)

        path = processing.download_track(track_id, metadata["preview"])

        embedding = processing.compute_embedding(track_id, path)

        data.add_track(track_id, embedding, metadata)

        data.save()

    # Get the genre of the track
    prediction = predict_track(embedding.reshape(1, -1))

    return JsonResponse({"genres": prediction})
