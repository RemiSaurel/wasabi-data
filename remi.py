import requests

from functions import get_data_from_file, get_field, API_URL


def generate_genres_analysis(genres_by_artist):
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
    response = requests.get(API_URL + "/api/v1/artist/country/popularity?limit=" + str(nb_countries))
    with open("analysis/nb_artists_by_countries.json", "w", encoding="utf-8") as f:
        f.truncate(0)
        f.write(str(response.json()))


def main_analysis(artist_list):
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
