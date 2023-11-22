import datetime
import json
from functions import get_data_from_file, get_field


def get_life_span(lifespan_by_artist):
    artist_career = {}

    with open("analysis/lifespan.json", "a", encoding="utf-8") as f:
        f.truncate(0)
        f.write("[\n")
        for (artist, lifeSpan) in lifespan_by_artist.items():
            begin = lifeSpan['begin'][:4]
            if (lifeSpan['ended']):
                end = lifeSpan['end'][:4]
            else:
                end = datetime.date.today().year
            if begin and end:
                duration = int(end) - int(begin)
            else:
                duration = 0
            f.write('{"artist": "' + artist + '", "begin": "' + str(begin) + '", "end": "' + str(
                end) + '", "duration": "' + str(duration) + '"},\n')
        f.write("]\n")


def generate_artists_infos(artist_list, albums_by_artist, deezer_fans):
    artist_infos = {}
    avg_likes_by_artist = {}
    with open("analysis/ch-artists_infos.json", "a", encoding="utf-8") as f:
        f.truncate(0)
        f.write("[\n")
        for artist in artist_list:
            nb_songs = 0
            sum_fans = 0
            nb_albums = len(albums_by_artist[artist])
            for album in albums_by_artist[artist]:
                nb_songs += len(album["songs"])
                count_albums = nb_albums
                if "deezerFans" not in album:
                    likes = 0
                    count_albums = count_albums-1
                else:
                    likes = album["deezerFans"]
                sum_fans += int(likes)
            avg_albums_fans = sum_fans/count_albums
            artist_infos[artist] = {"nbAlbums": nb_albums, "nbSongs": nb_songs,
                                    "deezerFans": deezer_fans[artist], "avgAlbumsFans": avg_albums_fans}
            f.write('{"artist": "' + artist + '", "nbAlbums": ' + str(
                nb_albums) + ', "nbSongs": ' + str(nb_songs) + ', "deezerFans": ' + str(deezer_fans[artist]) +
                    ', "avgAlbumsFans": ' + str(avg_albums_fans) + "},\n")
        f.write("]\n")

    return artist_infos


def main_data(artist_list):
    # READ DATA FROM FILES
    lifespan_by_artist = {}
    albums_by_artist = {}
    deezer_fans_by_artist = {}

    for artist in artist_list:
        artist_data = get_data_from_file("data/" + artist + ".json")
        lifespan_by_artist[artist] = get_field(artist_data, "lifeSpan")
        albums_by_artist[artist] = get_field(artist_data, "albums")
        deezer_fans_by_artist[artist] = get_field(artist_data, "deezerFans")
    generate_artists_infos(artist_list, albums_by_artist, deezer_fans_by_artist)
    get_life_span(lifespan_by_artist)
# json_object = json.dumps(albums_by_artist, indent=4)
# print(json_object)
