import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set up Spotify credentials (assuming you have set the environment variables)
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

def get_album_tracks(album_id):
    # Get the album's tracks
    tracks = sp.album_tracks(album_id)
    
    # Print each track's name
    for i, track in enumerate(tracks['items']):
        print(f"{i+1}: {track['name']}")

# Example album ID (replace this with the actual album ID you want to use)
album_id = '4aawyAB9vmqN3uQ7FjRGTy'  # Example: 'Starboy' by The Weeknd
get_album_tracks(album_id)
