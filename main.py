import time

from pathlib import Path

import requests as requests
import urllib.parse

# IMPORT YOUR FILE HERE
from remi import *

API_URL = "https://wasabi.i3s.unice.fr"

# FETCH ARTIST DATA FROM THE API
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


# GET A FIELD FROM AN ARTIST DATA
def get_field(artist_data, field):
    if artist_data is None:
        return []

    if field not in artist_data:
        print("No " + field + " found for " + artist_data["name"])
        return []

    print("Found " + str(len(artist_data[field])) + " " + field + " for " + artist_data["name"])
    return artist_data[field]


def request_artists():
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


if __name__ == "__main__":

    # LOAD ARTISTS FROM FILE
    with open("artists.txt", "r", encoding="utf-8") as f:
        ARTISTS = f.read().splitlines()

    # WARNING :
    # TURN ON TO GET NEW ARTISTS OR RELOAD SOME
    # request_artists()

    # GLOBAL ALBUMS TO USE
    albums = []

    # REMI VARIABLES
    unique_countries = set()
    unique_genres = set()
    genres_by_artist = {}
    location_by_artist = {}

    # READ DATA FROM FILES
    for artist in ARTISTS:
        with open("data/" + artist + ".json", "r", encoding="utf-8") as f:
            artist_data = eval(f.read())
            if artist_data is None:
                continue
            # PUT YOUR TREATMENT HERE TO AVOID MULTIPLE LOOPS / OPENING FILES
            albums.extend(get_field(artist_data, "albums"))
            genres_by_artist[artist] = get_field(artist_data, "genres")
            location_by_artist[artist] = get_field(artist_data, "location")

    # PRINT GLOBAL STATS
    print("Found " + str(len(albums)) + " albums in total")

    # REMI EXAMPLE
    unique_genres = generate_genres_analysis(genres_by_artist)
    unique_countries = generate_countries_analysis(location_by_artist)

    print("Found " + str(len(unique_genres)) + " unique genres in total")
    print("Found genres such as " + str(unique_genres))
    print("Found " + str(len(unique_countries)) + " unique countries in total")
    print("Found locations such as " + str(unique_countries))
