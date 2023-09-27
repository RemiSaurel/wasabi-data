from functions import get_data_from_file, get_field

# get the popularity of each artist and divide it by the number of genres they have
def artist_popularity_by_genre(artists):
    for artist in artists:
        artist_data = get_data_from_file("data/" + artist + ".json")
        artist_global_popularity = get_field(artist_data, "deezerFans")
        artist_genres = get_field(artist_data, "genres")
        if len(artist_genres) == 0:
            print(artist + " = " + str(artist_global_popularity))
        else:
            print(artist + " = " + str(round(artist_global_popularity / len(artist_genres))) + " & " + str(len(artist_genres)) + " genres")
    return ''


# regroup the genres by a global genre (alternative rock, ska rock, punk rock -> rock)
def regroup_genres(genres):
    return ""
