from pathlib import Path

import requests as requests
import urllib.parse

API_URL = "https://wasabi.i3s.unice.fr"

ARTISTS = [
    "Linkin Park",
    "Eminem",
    "Metallica",
    "The Beatles",
    "The Rolling Stones",
    "Queen",
    "Nirvana",
    "Guns N' Roses",
    "Red Hot Chili Peppers",
    "Pink Floyd",
    "Green Day",
    "Led Zeppelin",
    "Foo Fighters",
    "The Who",
    "U2",
    "The Doors",
    "Radiohead",
    "Jay-Z",
    "Coldplay",
]


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


def get_albums(filename):
    """Get all albums from an artist json file."""
    with open(filename, "r") as f:
        artist_data = eval(f.read())

    print("Found " + str(len(artist_data["albums"])) + " albums for " + artist_data["name"])
    # Print artist name | album title
    for album in artist_data["albums"]:
        print(artist_data["name"] + " | " + album["title"])
    return artist_data["albums"]


if __name__ == "__main__":
    # Write artist json data into a json file for each artist
    albums = []
    for artist in ARTISTS:
        # Check if artist data has already been fetched
        if Path("data/" + artist + ".json").is_file():
            print("Data for " + artist + " already fetched")
            continue

        print("Fetching data for " + artist)
        artist_data = fetch_artist(artist)
        with open("data/" + artist + ".json", "w") as f:
            f.write(str(artist_data))

    # Get all albums from all artists
    for artist in ARTISTS:
        albums.extend(get_albums("data/" + artist + ".json"))

    print("Found " + str(len(albums)) + " albums in total")
