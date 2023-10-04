import datetime

from functions import get_data_from_file, get_field


def get_life_span(lifespan_by_artist):
    artist_career ={}
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
            f.write('{"artist": "' + artist + '", "begin": "' + str(begin) +'", "end": "'+ str(end) +'", "duration": "'+str(duration)+ '"},\n')
        f.write("]\n")
def main_data(artist_list):
    # READ DATA FROM FILES
    lifespan_by_artist = {}
    for artist in artist_list:
        artist_data = get_data_from_file("data/" + artist + ".json")
        lifespan_by_artist[artist] = get_field(artist_data, "lifeSpan")
    get_life_span(lifespan_by_artist)
    #print("Chaimaeeeee"+str(lifespan_by_artist))
