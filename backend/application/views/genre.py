from django.http import JsonResponse
from rest_framework.decorators import api_view
from django.apps import apps
import logging
import os

from . import data

CONFIGURATION = apps.get_app_config("application")

MODELS = None

MODELS_PATH = os.path.join(CONFIGURATION.data_path, "genre_models.pickle")

def fit_model_for_genre(genre, albums):
    from sklearn.ensemble import BaggingClassifier 
    
    logging.info(f"Training model for genre {genre}")

    embeddings = data.get_embeddings()

    X = np.array((len(embeddings), embeddings[0].shape))
    y = np.array(len(embeddings))
    for i, (track_id, embedding) in enumerate(embeddings.items()):
        genre = data.get_genre(track_id)
        
        X[i] = embedding
        y[i] = genre
        
    
    
    
def predict_track(model, embedding):
    return model.predict(embedding)    

def train_model():
    
    logging.info("Training model")

    # Get all the tracks from the data
    albums = data.get_albums()
    
    for album in albums:
        train_model_for_genre(album["genre"])
    

def load_model():
    global MODELS

    # Check if the model is already loaded
    if MODELS is not None:
        return

    # Try load the model from the file
    try:
        with open(MODELS_PATH, "rb") as file:
            MODELS = pickle.load(file)
            
        logging.info("Loaded model")
    # If the file is not found, train the model
    except FileNotFoundError:
        logging.info("Model file not found, training model")
        
        albums = data.get_albums()
        
        # Group the albums by genre
        albums_by_genre = {}
        for album in albums:
            genre = album["genre"]
            
            if genre not in albums_by_genre:
                albums_by_genre[genre] = []
                
            albums_by_genre[genre].append(album)
        
        # Train a model for each genre
        for genre, albums in albums_by_genre.items():
            train_model_for_genre(genre, albums)
            
        MODELS = train_model()
        

@api_view(["GET"])
def genre_view(request):
    # Load the model
    load_model()
    
    # Get the track id from the request
    track_id = request.GET.get("track_id", "")

    # Check if the track_id is empty
    if track_id == "":
        return JsonResponse({"error": "No track specified"}, status=400)

    # Try to get the embedding from the data
    try:
        metadata, embedding = data.get_track(track_id)
    # If the embedding is not found, download the track, create the embedding and add it to the data
    except KeyError:
        metadata = deezer.get_track(track_id)

        path = processing.download_track(track_id, metadata["preview"])

        embedding = processing.compute_embedding(track_id, path)

        data.add_track(track_id, embedding, metadata)

        data.save()

    # Get the genre of the track
    
