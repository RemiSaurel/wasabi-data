# IMPORT YOUR FILE HERE
from functions import request_artists
from remi import *
from adam import *
import time
from chaimae import *

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
    #main_analysis(ARTISTS)
    # retrieve_artists()
    # clean_data()
    
    # CHAIMAE ANALYSIS
    main_data(ARTISTS)

    # ADAM ANALYSIS
    # artist_popularity_by_genre(ARTISTS)
    time_start = time.time()
    fetch_all_artists()
    time_end = time.time()
    print("Time elapsed : " + str(time_end - time_start) + " seconds")

    # PUT YOUR ANALYSIS HERE
