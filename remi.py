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
