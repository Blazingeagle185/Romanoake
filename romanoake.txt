from dotenv import load_dotenv
import os
import base64
from requests import post, get
import json
import requests
from unidecode import unidecode
#from flask import Flask, render_template

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
musixmatch = os.getenv("MUSIXMATCH_KEY")

#pp = Flask(__name__)

'''def index():
    return render_template('webSDK.html')
'''
def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return{"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist exists")
        return None
    return json_result[0]

def get_songs_by_artist(artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=IN"
    token = get_token()
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result

def get_track_id(track_name, artist_name):
    #gets track id from spotify (note might be a problem for later the track id from musixmatch and spotify might result in mismatching results)
    url1 = f"https://api.spotify.com/v1/search?q=track:{track_name}&type=track&limit=1"
    token = get_token()
    headers = get_auth_header(token)
    result = get(url1, headers=headers)
    json_result = json.loads(result.content)["tracks"]["items"]
    if json_result:
        spotify_id= json_result[0]['id']
    else: 
        spotify_id = "n"
    #gets track id from musixmatch
    url2 = "https://api.musixmatch.com/ws/1.1/track.search"
    params = {
        "q_track": track_name,
        "q_artist": artist_name,
        "apikey": musixmatch,
    }

    response = requests.get(url2, params=params)
    data = response.json()
    if data["message"]["body"]["track_list"]:
        musixmatch_id = data["message"]["body"]["track_list"][0]["track"]["track_id"]
    else:
        # Handle case where no tracks are found
        musixmatch_id = "n"
    #stores both track ids in an array for further use
    track_id = [spotify_id, musixmatch_id]
    
    return track_id
    
def get_lyrics(track_id):
    # Make a request to Musixmatch API to get lyrics
    response = requests.get(
        'https://api.musixmatch.com/ws/1.1/track.lyrics.get',
        params={'track_id': track_id[1], 'apikey': musixmatch}
    )
    data = response.json()
    # Extract lyrics from the response
    if 'message' in data and 'body' in data['message'] and 'lyrics' in data['message']['body']:
        return unidecode(data['message']['body']['lyrics']['lyrics_body'])
    else:
        return None

'''
    def get_playBack(track_name, artist_name):
    token = get_token()
    response = requests.put(
        "https://api.spotify.com/v1/me/player/play",
        headers=headers,
        json={'uris': [track_uri]}
    )
    error_data = response.json()
    error_message =  error_data.get("error", {}).get("message")
    if response.status_code == 200:
        print("Playback successful")
    elif response.status_code == 204:
        print("No content, playback started succesfully")
    else:
        print(f"Error starting playback: {response.status_code}, {error_message}")
'''


#token = get_token()
track_id = get_track_id("Come on Girls", "Anirudh Ravichander")
print(track_id)
#print(track_id)
lyrics = (get_lyrics(track_id))
print (lyrics)
'''get_playBack("Crew", "Brent Faiyaz")
#result = search_for_artist(token, "Kanye")
#print(result["name"
#artist_id = result["id"]
#songs = get_songs_by_artist(token, artist_id)

#for idx, song in enumerate(songs):
 #   print(f"{idx + 1}. {song['name']}")
'''