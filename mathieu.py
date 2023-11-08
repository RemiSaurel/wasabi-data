import json
import time
from tqdm import tqdm

import requests

from functions import get_data_from_file, get_field, API_URL

artist_info = []


def retrieve_artists(output_filename, start=0, step=200, nb_artists=1000):
    global artist_info  # Use the global artist_info variable
    pbar = tqdm(total=nb_artists, desc="Fetching artists")
    while start < nb_artists:
        pbar.update(step)
        new_data = fetch_artists(start)
        if new_data:
            merge_data(artist_info, new_data)  # Merge the new data with existing data
        start += step
    pbar.close()

    # Write into a json file
    with open("analysis/" + output_filename + ".json", "w", encoding="utf-8") as f:
        f.truncate(0)
        f.write(str(artist_info))


def fetch_artists(START):
    response = requests.get(API_URL + "/api/v1/artist_all/" + str(START))
    if response.status_code == 200:
        res = response.json()
        return generate_artist_data_mathieu(res)
    elif response.status_code == 429:
        print("Too many requests, waiting 10 seconds...")
        time.sleep(10)
        return fetch_artists(START)
    else:
        print(f"Error: Unable to fetch artists data. Status code: {response.status_code}")
        return None


def generate_artist_data_mathieu(data):
    artist_unique = []
    for artist in data:
        album_titles = []
        # Check if artist has a deezerFans field
        if "deezerFans" in artist:
            nbDeezerFans = artist["deezerFans"]
        else:
            nbDeezerFans = 0

        # Check if artist has a carrear field
        if "lifeSpan" in artist:
            carreer = artist["lifeSpan"]
            if carreer['ended'] == False:
                carreer['ended'] = 'false'
            if carreer['ended'] == True:
                carreer['ended'] = 'true'
            carreer['begin'] = carreer['begin'][:4]
            carreer['end'] = carreer['end'][:4]
        else:
            carreer = 0

        # Check if artist has an albums field
        if "albums" in artist:
            albums = artist["albums"]
            for album in albums:
                album_titles.append(album["title"])

        artist_entry = {
            '"artist": "' + str(artist["name"]) + "\", " + '"popularity": ' + str(
                nbDeezerFans)+ ", " + '"carrier": ' + json.dumps(carreer)
            + ", " + '"albums":' + json.dumps(album_titles)
        }
        artist_unique.append(artist_entry)
    return artist_unique


def merge_data(existing_data, new_data):
    for values in new_data:
        existing_data.append(values)


# OLD VALUE MATHIEU FROM HERE TO END
def generate_artists_analysis(artists_info, deezerfans, carrier):
    artist_album_popularity_creation = set()
    with open("analysis/artist_albums_creationGroupe.json", "a", encoding="utf-8") as f:
        f.truncate(0)
        f.write("[\n")
        for (artist, albums) in artists_info.items():
            artist_album = []
            for album in albums:
                title_album = album["title"]
                artist_album_popularity_creation.add(title_album)
                artist_album.append(title_album)
            f.write(
                '{"artist": "' + artist + ',"' + "popularity:" + str(deezerfans[artist]) + " start carrier:" + str(
                    carrier) + ', "albums": ' + str(artist_album) + "},\n")
        f.write("]\n")
    return artist_album_popularity_creation


def analysis(artist_list):
    # Mathieu VARIABLES
    artist_info = {}
    artist_popularity = {}
    artist_carrier = {}
    # READ DATA FROM FILES
    for artist in artist_list:
        artist_data = get_data_from_file("data/" + artist + ".json")
        # ARTIST EXAMPLE GET title from albums
        artist_info[artist] = get_field(artist_data, "albums")
        # ARTIST EXAMPLE GET deezerFans
        artist_popularity[artist] = get_field(artist_data, "deezerFans")
        # Artist GET carrier start
        artist_carrier[artist] = get_field(artist_data, "lifeSpan")
        # modify the fields to have it on the good way
        for (lifeSpan) in artist_carrier.items():
            lifeSpan[1]['begin'] = lifeSpan[1]['begin'][:4]
            if lifeSpan[1]['ended'] == False:
                lifeSpan[1]['ended'] = 'false'
            if lifeSpan[1]['ended'] == True:
                lifeSpan[1]['ended'] = 'true'
            if not lifeSpan[1]['end'] == '':
                lifeSpan[1]['end'] = lifeSpan[1]['end'][:4]
    #  # ARTIST EXAMPLE GET titles from albums
    unique_artist = generate_artists_analysis(artist_info, artist_popularity, artist_carrier)

    print("Found " + str(len(unique_artist)) + " artist title in total")
    print("Found title such as " + str(unique_artist))
