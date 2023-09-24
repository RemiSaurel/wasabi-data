import requests as requests

API_URL = "https://wasabi.i3s.unice.fr"

ARTISTS = [
    "Linkin Park",
    "Eminem",
    "Metallica"
]

def fetch_artist(artist_name):
    """Fetch artist data from the API."""
    response = requests.get(API_URL + "/api/v1/artist_all/name/" + artist_name)
    return response.json()


if __name__ == "__main__":
    # Write artist json data into a json file for each artist
    for artist in ARTISTS:
        artist_data = fetch_artist(artist)
        with open("data/" + artist + ".json", "w") as f:
            f.write(str(artist_data))
