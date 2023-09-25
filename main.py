# IMPORT YOUR FILE HERE
from functions import request_artists
from remi import *

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
    main_analysis(ARTISTS)

    # PUT YOUR ANALYSIS HERE
