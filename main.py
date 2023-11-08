# IMPORT YOUR FILE HERE
from functions import request_artists
from remi import *
from mathieu import *

if __name__ == "__main__":
    # LIST OF ARTISTS
    ARTISTS = []

    # LOAD ARTISTS FROM FILE
    with open("artists.txt", "r", encoding="utf-8") as f:
        ARTISTS = f.read().splitlines()

    # WARNING :
    # TURN ON TO GET NEW ARTISTS OR RELOAD SOME
    # request_artists(ARTISTS)

    # REMI ANALYSIS
    # main_analysis(ARTISTS)
    # retrieve_artists()
    # clean_data()

    # PUT YOUR ANALYSIS HERE
    # Mathieu Analyse
    # analysis(ARTISTS)
    retrieve_artists("artist_mathieu",nb_artists=10000)
