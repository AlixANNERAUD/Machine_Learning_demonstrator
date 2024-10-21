import os
import csv
import time
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.exceptions import SpotifyException

# Charger les clés API depuis les variables d'environnement
client_id = os.getenv("SPOTIPY_CLIENT_ID")
client_secret = os.getenv("SPOTIPY_CLIENT_SECRET")

# Authentification avec l'API Spotify
auth_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Fonction pour vérifier si une chanson est déjà dans le CSV
def is_song_in_csv(song_id, csv_filename):
    try:
        with open(csv_filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['track_id'] == song_id:
                    return True
    except FileNotFoundError:
        pass
    return False

# Fonction pour ajouter les informations d'une chanson au CSV
def add_song_to_csv(data, csv_filename):
    file_exists = os.path.isfile(csv_filename)
    
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        if not file_exists:
            writer.writeheader()
        writer.writerow(data)

# Fonction pour gérer les erreurs et les limitations de requêtes
def handle_spotify_exception(e):
    if isinstance(e, SpotifyException):
        if e.http_status == 429:  # Limite de requêtes atteinte
            retry_after = int(e.headers.get('Retry-After', 250))
            print(f"Limite d'API atteinte, attente de {retry_after} secondes...")
            time.sleep(retry_after)
            return True
        elif e.http_status == 404:  # Ressource non trouvée
            print("Ressource non trouvée, passage à l'élément suivant...")
            return False
    else:
        print(f"Erreur inconnue : {e}")
        return False

# Fonction principale pour récupérer les informations d'une playlist
def scrape_playlist(playlist_id, csv_filename):
    try:
        playlist = sp.playlist(playlist_id)
        print(f"Playlist : {playlist['name']}")
    except SpotifyException as e:
        if not handle_spotify_exception(e):
            return

    for item in playlist['tracks']['items']:

        try:
            track = item['track']
            track_id = track['id']

            # Si la chanson est déjà dans le CSV, on la saute
            if is_song_in_csv(track_id, csv_filename):
                print(f"La chanson {track['name']} est déjà dans le CSV.")
                continue

            # Récupérer les informations sur l'album
            album = track['album']
            album_data = {
                'album_id': album['id'],
                'release_date': album['release_date'],
                'release_date_precision': album['release_date_precision'],
                'album_restrictions': album.get('restrictions', 'none')
            }

            # Récupérer les informations sur les artistes
            artists = [{'artist_id': artist['id'], 'artist_name': artist['name']} for artist in track['artists']]

            # Récupérer les informations sur la chanson
            track_data = {
                'track_id': track_id,
                'track_name': track['name'],
                'track_duration_ms': track['duration_ms'],
                'track_explicit': 'yes' if track['explicit'] else 'no',
                'track_restrictions': track.get('restrictions', 'none'),
                'track_popularity': track['popularity'],
                'track_preview_url': track['preview_url']
            }

            # Récupérer les features audio de la chanson
            audio_features = sp.audio_features(track_id)[0]
            if audio_features:
                audio_features_data = {
                    'acousticness': audio_features['acousticness'],
                    'analysis_url': audio_features['analysis_url'],
                    'danceability': audio_features['danceability'],
                    'energy': audio_features['energy'],
                    'instrumentalness': audio_features['instrumentalness'],
                    'key': audio_features['key'],
                    'liveness': audio_features['liveness'],
                    'loudness': audio_features['loudness'],
                    'mode': audio_features['mode'],
                    'speechiness': audio_features['speechiness'],
                    'tempo': audio_features['tempo'],
                    'time_signature': audio_features['time_signature'],
                    'valence': audio_features['valence']
                }
            else:
                audio_features_data = {key: None for key in ['acousticness', 'analysis_url', 'danceability', 'energy', 
                                                             'instrumentalness', 'key', 'liveness', 'loudness', 'mode', 
                                                             'speechiness', 'tempo', 'time_signature', 'valence']}
            
            # Combiner toutes les données dans une seule entrée
            combined_data = {**album_data, **track_data, **audio_features_data, 'artists': artists}

            # Ajouter les informations au CSV
            add_song_to_csv(combined_data, csv_filename)
            print(f"Ajouté : {track['name']}")
            time.sleep(random.randint(1, 3)/100)  # Attendre entre 10 et 30 millisecondes avant de passer à la chanson suivante 

        except SpotifyException as e:
            if not handle_spotify_exception(e):
                continue

# Liste d'ID de playlists et nom du fichier CSV
playlists = []  # À remplacer par tes playlists
csv_filename = 'spotify_tracks.csv'

# Scraper chaque playlist
for playlist_id in playlists:
    scrape_playlist(playlist_id, csv_filename)
    time.sleep(random.randint(10, 40))  # Attendre entre 1 et 3 secondes avant de passer à la playlist suivante
