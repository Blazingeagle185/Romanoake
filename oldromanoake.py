import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep
import os
from dotenv import load_dotenv
import logging

load_dotenv()

scope = "user-read-playback-state,user-modify-playback-state"


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"),
                                               client_secret=os.getenv("CLIENT_SECRET"),
                                               redirect_uri="http://localhost:1234",
                                               scope=scope))


search = "Take My Hand Okpop"
result = sp.search(search)
logging.debug("Spotify search result: %s", result)
data = result['tracks']['items'][0]



track_uri = result['tracks']['items'][0]['uri']

# Shows playing devices
res = sp.devices()


# Change track
sp.start_playback(uris=[track_uri])

# Change volume
sp.volume(75)
res = sp.current_playback()

pprint(data)


