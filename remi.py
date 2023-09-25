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


def generate_countries_analysis(location_by_artist):
    unique_countries = set()
    with open("analysis/countries.json", "a", encoding="utf-8") as f:
        f.truncate(0)
        f.write("[\n")
        for (artist, location) in location_by_artist.items():
            if location is None:
                continue
            country = location["country"]
            unique_countries.add(country)
            f.write('{"artist": "' + artist + '", "country": "' + country + '"},\n')
        f.write("]\n")
    return unique_countries

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

    # READ DATA FROM FILES
    for artist in artist_list:
        artist_data = get_data_from_file("data/" + artist + ".json")

        # REMI EXAMPLE
        genres_by_artist[artist] = get_field(artist_data, "genres")
        location_by_artist[artist] = get_field(artist_data, "location")

    # REMI EXAMPLE
    unique_genres = generate_genres_analysis(genres_by_artist)
    unique_countries = generate_countries_analysis(location_by_artist)
    get_artist_number_by_country(100)

    print("Found " + str(len(unique_genres)) + " unique genres in total")
    print("Found genres such as " + str(unique_genres))
    print("Found " + str(len(unique_countries)) + " unique countries in total")
    print("Found locations such as " + str(unique_countries))
