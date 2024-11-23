import json


def get_artist_pairs(json_string: str) -> list[tuple[str, str]]:
    data = json.loads(json_string.replace("'", '"'))
    return [(artist["artist_id"], artist["artist_name"]) for artist in data]


def get_artist_string(json_string: str) -> str:
    """Concatenate the artist names"""
    data = json.loads(json_string.replace("'", '"'))
    return ", ".join(artist["artist_name"] for artist in data)
