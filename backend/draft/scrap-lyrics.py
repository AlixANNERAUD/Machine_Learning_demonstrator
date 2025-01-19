import numpy as np
import lyricsgenius
import json
import os
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
import time
from spotipy.exceptions import SpotifyException


def get_lyrics(song_title, artist_name):
    try:
        song = genius.search_song(title=song_title, artist=artist_name)
        if song:
            return song.lyrics
        else:
            print(f"Paroles non trouvées pour '{song_title}' par '{artist_name}'.")
            return None
    except Exception as e:
        print(f"Erreur lors de la récupération des paroles : {e}")
        return None


def save_lyrics_to_json(lyrics, id_song, file_name="lyrics.json"):
    data = {
        "id_song": id_song,
        "lyrics": lyrics
    }

    try:
        # Lire le fichier existant ou initialiser un tableau vide
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                content = json.load(f)
        except FileNotFoundError:
            content = []

        # Vérifier si la chanson est déjà présente
        if any(entry['id_song'] == id_song for entry in content):
            print(f"Les paroles de la chanson ID {id_song} sont déjà enregistrées.")
            return

        # Ajouter les nouvelles données
        content.append(data)

        # Écrire les données mises à jour dans le fichier
        with open(file_name, 'w', encoding='utf-8') as f:
            json.dump(content, f, ensure_ascii=False, indent=4)

        print(f"Les paroles de la chanson ID {id_song} ont été enregistrées dans {file_name}.")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement : {e}")


# Handle API exceptions and request limits
def handle_spotify_exception(e):
    if isinstance(e, SpotifyException):
        if e.http_status == 429:  # Rate limit exceeded
            retry_after = int(e.headers.get("Retry-After", 250))
            print(f"Rate limit hit, waiting for {retry_after} seconds...")
            time.sleep(retry_after)
            return True
        elif e.http_status == 404:  # Resource not found
            print("Resource not found, skipping to next...")
            return False
    else:
        print(f"Unknown error: {e}")
        return False

def get_tracks_info_in_batches_from_spotify(spotify_ids):
    """
    Récupère les noms de chansons et les noms d'artistes principaux pour une liste d'IDs Spotify, par lots de 100.
    
    Args:
        spotify_ids (list): Liste des IDs Spotify des chansons.
    
    Returns:
        list: Liste de dictionnaires contenant les IDs, titres et artistes principaux.
    """

    # Résultats
    tracks_info = []

    # Traitement par lots de 100
    batch_size = 100
    for i in range(0, len(spotify_ids), batch_size):
        print(i)
        batch_ids = spotify_ids[i:i + batch_size]
        try:
            response = sp.tracks(batch_ids)
            for track in response['tracks']:
                if track:  # Vérifie que la piste existe
                    tracks_info.append({
                        'id': track['id'],
                        'name': track['name'],
                        'artist': track['artists'][0]['name']  # Artiste principal
                    })
        except SpotifyException as e:
            handle_spotify_exception(e)
            continue
    
    return tracks_info

def is_song_in_json(song_id, json_file_name="lyrics.json"):
    try:
        with open(json_file_name, mode='r', encoding='utf-8') as file:
            content = json.load(file)
            for entry in content:
                if entry['id_song'] == song_id:
                    return True
        return False
    except FileNotFoundError:
        return False

def scrape_lyrics_from_spotify_ids(spotify_ids, json_file_name="lyrics.json"):
    # Récupérer les informations des pistes
    tracks_info = get_tracks_info_in_batches_from_spotify(spotify_ids)
    print(len(tracks_info))
    
    # Ouvrir le fichier json en mode écriture
    indice_suivi = 0
    for track in tracks_info:
        if not(is_song_in_json(spotify_ids[indice_suivi], json_file_name)):
            lyrics = get_lyrics(track['name'], track['artist'])
            save_lyrics_to_json(lyrics, track['id'], file_name=json_file_name)
            print(f"Les paroles de la chanson '{track['name']}' par '{track['artist']}' ont été enregistrées dans le fichier JSON.")
            time.sleep(1)  # Pause d'une seconde entre les requêtes
        else:
            print("Chanson déjà enregistrée dans le fichier json.")
        print(f"{indice_suivi = }")
        indice_suivi += 1

if __name__ == "__main__":
    # Charger les clés API depuis les variables d'environnement
    SPOTIPY_CLIENT_ID = os.getenv("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
    GENIUS_CLIENT_ID = os.getenv('GENIUS_CLIENT_ID')
    GENIUS_CLIENT_SECRET = os.getenv('GENIUS_CLIENT_SECRET')

    # Authentification avec les API
    auth_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
    sp = Spotify(auth_manager=auth_manager)
    genius = lyricsgenius.Genius(GENIUS_CLIENT_ID)
    print("API ok")

    path = './embeddings_24-11-26/'
    id_embeddings = np.load(path + 'id_embeddings_330.npy')
    embeddings = np.load(path + 'embeddings_330.npy')
    print(embeddings)

    print("Début du scrapping")
    # Test avec les 500 premières chansons
    scrape_lyrics_from_spotify_ids(id_embeddings[:500])




