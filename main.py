import time

from pathlib import Path

import requests as requests
import urllib.parse

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
                with open(artist_json_path, "r") as f:
                    artist_data = eval(f.read())
                    if artist_data is None:
                        time.sleep(3)
                        print("Fetching data for " + artist)
                        artist_data = fetch_artist(artist)
                        with open(artist_json_path, "w") as f:
                            f.write(str(artist_data))
                    else:
                        print("Using cached data for " + artist)
                        fetched_artists[artist] = artist_data
        else:
            time.sleep(3)
            print("Fetching data for " + artist)
            artist_data = fetch_artist(artist)
            with open(artist_json_path, "w") as f:
                f.write(str(artist_data))


if __name__ == "__main__":
    albums = []
    genres_by_artist = {}
    location_by_artist = {}

    all_countries = set()
    all_genres = set()

    with open("artists.txt", "r") as f:
        ARTISTS = f.read().splitlines()

    # TURN ON TO GET NEW ARTISTS OR RELOAD SOME
    # request_artists()

    # Get all albums from all artists
    for artist in ARTISTS:
        with open("data/" + artist + ".json", "r") as f:
            artist_data = eval(f.read())
            if artist_data is None:
                continue
            albums.extend(get_field(artist_data, "albums"))
            genres_by_artist[artist] = get_field(artist_data, "genres")
            location_by_artist[artist] = get_field(artist_data, "location")

    for (artist, genres) in genres_by_artist.items():
        for genre in genres:
            all_genres.add(genre)
        print(artist + " : " + str(genres))

    for (artist, location) in location_by_artist.items():
        if location is None:
            continue
        country = location["country"]
        all_countries.add(country)
        print(artist + " : " + str(country))

    print("Found " + str(len(albums)) + " albums in total")
    print("Found " + str(len(all_genres)) + " genres in total")
    print("Found genres such as " + str(all_genres))
    print("Found " + str(len(all_countries)) + " countries in total")
    print("Found locations such as " + str(all_countries))
