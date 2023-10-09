import time
import urllib
from pathlib import Path

import requests

API_URL = "https://wasabi.i3s.unice.fr"


def fetch_artist(artist_name):
    """Fetch artist data from the API."""
    # Encode the artist name to avoid errors, e.g. "AC/DC" -> "AC%2FDC"
    artist_encoded = urllib.parse.quote(artist_name)
    print("Encoded : " + artist_encoded)
    response = requests.get(API_URL + "/api/v1/artist_all/name/" + artist_encoded)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: Unable to fetch artist data. Status code: {response.status_code}")
        return None


def get_field(artist_data, field):
    """Get a field from an artist data dictionary."""
    print("Getting " + field + " from " + artist_data["name"])
    if artist_data is None:
        return []

    if field not in artist_data:
        print("No " + field + " found for " + artist_data["name"])
        return []

    return artist_data[field]


def request_artists(ARTISTS):
    # Dictionary to keep track of fetched artist data
    fetched_artists = {}

    # Write artist json data into a json file for each artist
    for artist in ARTISTS:
        artist_json_path = Path("data") / f"{artist}.json"

        # Check if artist data has already been fetched
        if artist_json_path.is_file():
            if artist not in fetched_artists:
                # Check if the file contains "None", if yes, fetch the data again
                with open(artist_json_path, "r", encoding="utf-8") as f:
                    artist_data = eval(f.read())
                    if artist_data is None:
                        time.sleep(3)
                        print("Fetching data for " + artist)
                        artist_data = fetch_artist(artist)
                        f.write(str(artist_data))
                    else:
                        print("Using cached data for " + artist)
                        fetched_artists[artist] = artist_data
        else:
            time.sleep(3)
            print("Fetching data for " + artist)
            artist_data = fetch_artist(artist)
            with open(artist_json_path, "w", encoding="utf-8") as f:
                f.write(str(artist_data))


def get_data_from_file(file):
    """Get data from a file."""
    with open(file, "r", encoding="utf-8") as f:
        artist_data = eval(f.read())
        if artist_data is not None:
            return artist_data
        else:
            return None
