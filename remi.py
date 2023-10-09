import json
import time
from tqdm import tqdm

import requests

from functions import get_data_from_file, get_field, API_URL

artist_info = {}  # Use a dictionary with country names as keys


def format_data():
    """Format the data from full_countries.json into a list of dictionaries.
    The goal is to have a list of dictionaries with the following format:
    [
      {
        "country": "France",
        "artists": [
          {
            "artist": "Daft Punk",
            "genres": ["electronic", "house", "techno"],
            "nbAlbums": 4,
            "nbSongs": 40,
            "deezerFans": 1000000
          },
          ...
          other artists...
        ]
      },
      other countries...
    ]"""

    output_data = {}

    with open("analysis/full_countries.json", "r", encoding="utf-8") as f:
        input_data = eval(f.read())
        for country, artists_list in input_data.items():
            for artist in artists_list:
                artist_entry = {
                    "artist": artist["artist"],
                    "genres": artist["genres"],
                    "nbAlbums": artist["nbAlbums"],
                    "nbSongs": artist["nbSongs"],
                    "deezerFans": artist["deezerFans"]
                }
                if country not in output_data:
                    output_data[country] = []
                output_data[country].append(artist_entry)

    with open("analysis/full_countries_clean.json", "w", encoding="utf-8") as f:
        f.truncate(0)
        f.write("[\n")
        for country, artists_list in output_data.items():
            f.write('{"country": "' + country + '", "artists": ' + json.dumps(artists_list) + "},\n")
        f.write("]\n")


def retrieve_artists(output_filename, start=0, step=200, nb_artists=1000):
    """Retrieve artists from the API and write them into a json file.
    Different parameters can be used to retrieve artists:
    :param str output_filename: The name of the output file
    :param int start: The index of the first artist to retrieve
    :param int step: The number of artists to retrieve
    :param int nb_artists: The total number of artists to retrieve
    """
    global artist_info  # Use the global artist_info variable
    pbar = tqdm(total=nb_artists, desc="Fetching artists")

    while start < nb_artists:
        pbar.update(step)

        new_data = fetch_artists(start)
        if new_data:
            merge_data(artist_info, new_data)  # Merge the new data with existing data
        start += step
        # Wait 1 second to avoid being blocked by the API
        # time.sleep(1)

    pbar.close()

    # Write into a json file
    with open("analysis/" + output_filename + ".json", "w", encoding="utf-8") as f:
        f.truncate(0)
        f.write(str(artist_info))


def fetch_artists(START):
    """Fetch artists from the API and return a dictionary with country names as keys
    and a list of artists as values for each artist: artist name, genres, number of albums,
    number of songs, number of deezer fans
    :param int START: The index of the first artist to retrieve
    """

    response = requests.get(API_URL + "/api/v1/artist_all/" + str(START))
    if response.status_code == 200:
        res = response.json()
        return generate_countries_artist_data(res)

    elif response.status_code == 429:
        print("Too many requests, waiting 10 seconds...")
        time.sleep(10)
        return fetch_artists(START)
    else:
        print(f"Error: Unable to fetch artists data. Status code: {response.status_code}")
        return None


def generate_countries_artist_data(data):
    """Generate a dictionary with country names as keys and a list of artists as values
    for each artist: artist name, genres, number of albums, number of songs, number of deezer fans
    :param dict data: The data from the API
    """
    country_artists = {}
    for artist in data:
        nb_albums = len(artist["albums"])
        country = artist["location"]["country"]
        genres = artist["genres"]

        # Check if artist has a deezerFans field
        if "deezerFans" in artist:
            nbDeezerFans = artist["deezerFans"]
        else:
            nbDeezerFans = 0

        nb_songs = 0
        for album in artist["albums"]:
            nb_songs += len(album["songs"])

        artist_entry = {
            "artist": artist["name"],
            "genres": genres,
            "nbAlbums": nb_albums,
            "nbSongs": nb_songs,
            "deezerFans": nbDeezerFans
        }

        if country not in country_artists:
            country_artists[country] = []

        country_artists[country].append(artist_entry)

    return country_artists


def merge_data(existing_data, new_data):
    """Merge new data with existing data.
    :param dict existing_data: The existing data
    :param dict new_data: The new data
    """
    for country, artists in new_data.items():
        if country in existing_data:
            existing_data[country].extend(artists)
        else:
            existing_data[country] = artists


def generate_genres_analysis(genres_by_artist):
    """OLD ANALYSIS FUNCTION"""

    unique_genres = set()
    with open("analysis/genres.json", "a", encoding="utf-8") as f:
        f.truncate(0)
        f.write("[\n")
        for (artist, genres) in genres_by_artist.items():
            for genre in genres:
                unique_genres.add(genre)
            f.write('{"artist": "' + artist + '", "genres": ' + str(genres) + "},\n")
        f.write("]\n")
    return unique_genres


def generate_countries_analysis(location_by_artist, artists_infos):
    """OLD ANALYSIS FUNCTION"""

    country_artists = {}
    with open("analysis/countries.json", "a", encoding="utf-8") as f:
        f.truncate(0)
        f.write("[\n")

        # For each artist / location, add the country with the artist name
        # If 2 artists have the same country, it will be added only once
        for (artist, location) in location_by_artist.items():
            if location is None:
                continue
            country = location['country']
            if country not in country_artists:
                country_artists[country] = []
            country_artists[country].append(artist)
        # For each country, add the artists
        for (country, artists) in country_artists.items():
            artist_data = []
            for artist in artists:
                artist_data.append({"artist": artist, "genres": artists_infos[artist]["genres"],
                                    "nbAlbums": artists_infos[artist]["nbAlbums"],
                                    "nbSongs": artists_infos[artist]["nbSongs"],
                                    "deezerFans": artists_infos[artist]["deezerFans"]})
            f.write('{"country": "' + country + '", "artists": ' + str(artist_data) + "},\n")
        f.write("]\n")
    return country_artists


def generate_artists_infos(artist_list, genres_by_artist, albums_by_artist, deezer_fans):
    """OLD ANALYSIS FUNCTION"""

    artist_infos = {}
    with open("analysis/artists_infos.json", "a", encoding="utf-8") as f:
        f.truncate(0)
        f.write("[\n")
        for artist in artist_list:
            nb_songs = 0
            nb_albums = len(albums_by_artist[artist])
            for album in albums_by_artist[artist]:
                nb_songs += len(album["songs"])
            artist_infos[artist] = {"genres": genres_by_artist[artist], "nbAlbums": nb_albums, "nbSongs": nb_songs,
                                    "deezerFans": deezer_fans[artist]}
            f.write('{"artist": "' + artist + '", "genres": ' + str(genres_by_artist[artist]) + ', "nbAlbums": ' + str(
                nb_albums) + ', "nbSongs": ' + str(nb_songs) + ', "deezerFans": ' + str(deezer_fans[artist]) + "},\n")
        f.write("]\n")
    return artist_infos


def get_artist_number_by_country(nb_countries):
    """Find the number of artists by country from the API and write them into a json file."""
    response = requests.get(API_URL + "/api/v1/artist/country/popularity?limit=" + str(nb_countries))
    with open("analysis/nb_artists_by_countries.json", "w", encoding="utf-8") as f:
        f.truncate(0)
        f.write(str(response.json()))


def main_analysis(artist_list):
    """OLD ANALYSIS FUNCTION"""

    # REMI VARIABLES
    unique_countries = set()
    unique_genres = set()
    genres_by_artist = {}
    location_by_artist = {}
    albums_by_artist = {}
    deezer_fans_by_artist = {}
    artist_infos = {}
    countries_analysis = {}

    # READ DATA FROM FILES
    for artist in artist_list:
        artist_data = get_data_from_file("data/" + artist + ".json")

        # REMI EXAMPLE
        genres_by_artist[artist] = get_field(artist_data, "genres")
        location_by_artist[artist] = get_field(artist_data, "location")
        albums_by_artist[artist] = get_field(artist_data, "albums")
        deezer_fans_by_artist[artist] = get_field(artist_data, "deezerFans")

    # REMI EXAMPLE
    unique_genres = generate_genres_analysis(genres_by_artist)
    artist_infos = generate_artists_infos(artist_list, genres_by_artist, albums_by_artist, deezer_fans_by_artist)
    countries_analysis = generate_countries_analysis(location_by_artist, artist_infos)
    get_artist_number_by_country(100)

    print("Found " + str(len(unique_genres)) + " unique genres in total")
    print("Found genres such as " + str(unique_genres))
