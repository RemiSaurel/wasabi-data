import requests
import time

from functions import API_URL

# TODO test the method when the api will be operational
def fetch_all_artists():
    """Fetch all artists from the API and write them to a json file."""
    start = 0
    all_data = {"artists" : [], "genres" : []}
    while start < 75000:
        print("Fetching artists from " + str(start) + " to " + str(start + 200))
        data = fetch_artists(start)

        for genre in data['genres']:
            if genre not in all_data['genres']:
                all_data['genres'].append(genre)
        all_data['artists'] += data['artists']

        start += 200
    write_json_genres(all_data['artists'], all_data['genres'])


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


def artist_popularity_by_genre(data):
    """Get the popularity of each artist and divide it by the number of genres they have
    :data dict: The response from the API
    """
    genres = []
    artists = []
    for artist in data:
        artist_global_popularity = artist["deezerFans"] if "deezerFans" in artist else 0
        artist_genres = artist["genres"]
        nb_albums = len(artist["albums"])
        artist_country = artist["location"]["country"]
        nb_songs = 0
        for album in artist["albums"]:
            nb_songs += len(album["songs"])

        if len(artist_genres) == 0:
            artist_genres = ["Unknown"]
        artists_infos = {
            "name": artist["name"],
            "popularity": artist_global_popularity,
            "genres": artist_genres,
            "nbAlbums": nb_albums,
            "nbSongs": nb_songs,
            "country": artist_country
        }
        artists.append(artists_infos)
        for genre in artist_genres:
            if genre not in genres:
                genres.append(genre)
    return {"artists": artists, "genres": genres}


def write_json_genres(artists, genres):
    """Write the artists and genres data into a json file
    :param list artists: The list of artists
    :param list genres: The list of genres
    """

    with open("analysis/adam_genre.json", "a", encoding="utf-8") as f:
        f.truncate(0)
        f.write("[")
        for genre in genres:
            f.write('{"genre": "' + str(genre) + '",')
            f.write(' "artists": [')
            for artist in artists:
                if genre in artist["genres"]:
                    artist_name = artist["name"]
                    nb_albums = artist["nbAlbums"]
                    nb_songs = artist["nbSongs"]
                    country = artist["country"]
                    popularity_by_genre = round(artist["popularity"] / len(artist["genres"]))
                    f.write('  {"name": "' + artist_name + '",'
                            + '"nbFans": ' + str(popularity_by_genre) + ','
                            + ' "nbFans": ' + str(popularity_by_genre) + ','
                            + '"nbAlbums": ' + str(nb_albums) + ','
                            + '"nbSongs": ' + str(nb_songs) + ','
                            + '"country": ' + str(country) + '},')
            f.write(' ]')
            f.write("},")
        f.write("]")


#TODO
# regroup the genres by a global genre (alternative rock, ska rock, punk rock -> rock)
def regroup_genres(genres):
    return ""
