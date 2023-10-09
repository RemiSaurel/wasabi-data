import json

import requests
import time

from functions import API_URL


def artist_popularity_by_genre(data):
    """Get the popularity of each artist and divide it by the number of genres they have
    :artists dict: The response from the API
    """
    genres = []
    artists = []
    for artist in data:
        artist_global_popularity = artist["deezerFans"] if "deezerFans" in artist else 0
        artist_genres = artist["genres"]
        if len(artist_genres) == 0:
            artist_genres = ["Unknown"]
        artists_infos = {"name": artist["name"], "popularity": artist_global_popularity, "genres": artist_genres}
        artists.append(artists_infos)
        for genre in artist_genres:
            if genre not in genres:
                genres.append(genre)
        # print(artist["name"] + " = " + str(popularity_by_genre) + " fans & " + str(
        #     len(artist_genres)) + " genres " + str(artist_genres))
    # print("Total genres : " + str(len(genres)))
    # print(genres)
    # print(artists)
    write_json_genres(artists, genres)


def fetch_artists(START=0):
    """Fetch artists from the API and return a dictionary with country names as keys
    and a list of artists as values for each artist: artist name, genres, number of albums,
    number of songs, number of deezer fans
    :param int START: The index of the first artist to retrieve
    """

    response = requests.get(API_URL + "/api/v1/artist_all/" + str(START))
    if response.status_code == 200:
        res = response.json()
        return artist_popularity_by_genre(res)
    elif response.status_code == 429:
        print("Too many requests, waiting 10 seconds...")
        time.sleep(10)
        return fetch_artists(START)
    else:
        print(f"Error: Unable to fetch artists data. Status code: {response.status_code}")
        return None


# regroup the genres by a global genre (alternative rock, ska rock, punk rock -> rock)
def regroup_genres(genres):
    return ""


def write_json_genres(artists, genres):
    with open("analysis/adam_genre.json", "a", encoding="utf-8") as f:
        f.truncate(0)
        f.write("[\n")
        print(artists)
        print(genres)
        for genre in genres:
            f.write('{"genre": "' + str(genre) + '",\n')
            f.write(' "artists": [\n')
            for artist in artists:
                if genre in artist["genres"]:
                    artist_name = artist["name"]
                    popularity_by_genre = round(artist["popularity"] / len(artist["genres"]))
                    f.write('  {"name": "' + artist_name + '", "nbFans": ' + str(popularity_by_genre) + '},\n')
            f.write(' ]\n')
            f.write("},\n")
        f.write("]\n")


