from functions import get_data_from_file, get_field


def generate_artists_analysis(artists_info, deezerFans):
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
                '{"artist": "' + artist + ',"' + "popularity:" + str(deezerFans[artist]) + ', "albums": ' + str(artist_album) + "},\n")
        f.write("]\n")
    return artist_album_popularity_creation


def analysis(artist_list):
    # Mathieu VARIABLES
    artist_info = {}
    artist_popularity = {}
    # READ DATA FROM FILES
    for artist in artist_list:
        artist_data = get_data_from_file("data/" + artist + ".json")
        # ARTIST EXAMPLE GET title from albums
        artist_info[artist] = get_field(artist_data, "albums")
        # ARTIST EXAMPLE GET deezerFans
        artist_popularity[artist] = get_field(artist_data, "deezerFans")

    #  # ARTIST EXAMPLE GET titles from albums
    unique_artist = generate_artists_analysis(artist_info, artist_popularity)

    print("Found " + str(len(unique_artist)) + " artist title in total")
    print("Found title such as " + str(unique_artist))
