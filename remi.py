from pathlib import Path

from main import get_data_from_file, get_field


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


def main_analysis(artist_list):
    # REMI VARIABLES
    unique_countries = set()
    unique_genres = set()
    genres_by_artist = {}
    location_by_artist = {}

    # READ DATA FROM FILES
    for artist in artist_list:
        artist_data = get_data_from_file(Path("data") / f"{artist}.json")

        # REMI EXAMPLE
        genres_by_artist[artist] = get_field(artist_data, "genres")
        location_by_artist[artist] = get_field(artist_data, "location")

    # REMI EXAMPLE
    unique_genres = generate_genres_analysis(genres_by_artist)
    unique_countries = generate_countries_analysis(location_by_artist)

    print("Found " + str(len(unique_genres)) + " unique genres in total")
    print("Found genres such as " + str(unique_genres))
    print("Found " + str(len(unique_countries)) + " unique countries in total")
    print("Found locations such as " + str(unique_countries))
