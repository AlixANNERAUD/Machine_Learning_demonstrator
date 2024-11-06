import csv

from modules import scrap

client = scrap.load_spotify_client()

# Read CSV file: "tracks.csv"
# Get all "album_id" from the CSV file

album_ids = []
with open("tracks.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        album_id = row.get("album_id")
        if album_id:
            album_ids.append(album_id)

# Remove duplicates
album_ids = list(set(album_ids))

print(f"Found {len(album_ids)} unique album IDs")

with open("albums.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["album_id", "genres"])

    for i, album_id in enumerate(album_ids):
        album = client.album(album_id)
        genres = album["genres"]
        if genres:
            writer.writerow([album_id, genres])
            print([album_id, genres])
        print(f"{i+1}/{len(album_ids)}", end="\r")

print("Done!")
