# shows audio analysis for the given track

from spotipy.oauth2 import SpotifyClientCredentials
import json
import spotipy
import time
import sys
import os
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from flask import jsonify
from scipy.spatial import distance
import numpy as np

def cosine_similarity(vector1, vector2):
    return 1 - distance.cosine(vector1, vector2)
'''
similarity = cosine_similarity(reference_timbre, current_timbre)
print(f"Cosine Similarity: {similarity}")

threshold = 0.9  # Set based on experimentation
is_singing = similarity > threshold
print(f"Is Singing: {is_singing}")
'''
load_dotenv()

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"),
                                               client_secret=os.getenv("CLIENT_SECRET"),
                                               redirect_uri="http://localhost:1234",
                                               scope=scope))


song = "uuuu"
result = sp.search(song, limit = 1)


track_info = result['tracks']['items'][0]
data = track_info
track_uri = track_info['uri']

tid = track_uri


analysis = sp.audio_analysis(tid)

segments = analysis.get('segments')


analysis_dict = {}

timestamp_start = 1.77
timestamp_end = 9.11
for i, segment in enumerate(segments):
    if (segment['start'] > timestamp_start) and ((segment['duration'] + segment['start']) < timestamp_end) and (segment['confidence'] > 0.5):
        # Add segment to the dictionary with a unique key
        analysis_dict[f"segment_{i}"] = segment
    print(type(segment))
#for i, segment in enumerate(analysis_dict):
j = 0
#while(len(analysis_dict) > 0):
temp_analysis = {}

j = 0
timbre_groupings = {}
group_number = 1

while(analysis_dict):
    temp_analysis = {}
    for segment_key, segment_value in analysis_dict.items():
            first_key = next(iter(analysis_dict))
            first_value = analysis_dict[first_key]
            # Retrieve the timbre arrays from the current segment and the first segment
            timbre1 = np.array(analysis_dict.get(segment_key, {}).get('timbre'))
            timbre2 = np.array(first_value['timbre'])
            # Check that both timbre arrays are not None before calculating cosine similarity
            if timbre1 is not None and timbre2 is not None:
                # Calculate cosine similarity
                cosine_similarity = np.dot(timbre1, timbre2) / (np.linalg.norm(timbre1) * np.linalg.norm(timbre2))
                # Now you can compare the cosine similarity
                if cosine_similarity > 0.5:
                    # Add the segment to temp_analysis using its key
                    temp_analysis[segment_key] = segment_value
            else:
                print(f"Timbre data is missing for key {segment_key}")
    if len(temp_analysis) == 1:
        single_key = next(iter(temp_analysis))
        timbre_groupings[f'group_{group_number}'] = {single_key: temp_analysis[single_key]}
        group_number += 1
        del analysis_dict[single_key]
        continue

    while(temp_analysis):
            # Take the first entry in the temporary dictionary as the reference
            reference_key, reference_segment = next(iter(temp_analysis.items()))
            reference_timbre = np.array(reference_segment['timbre'])
            # Initialize the current group with the reference
            current_group = {reference_key: reference_segment}

            # List to hold keys of timbres that will be grouped together
            keys_to_remove = [reference_key]  # Include the reference key itself

            for key, segment in temp_analysis.items():
                if key == reference_key:
                    continue  # Skip the reference segment

                timbre_vector = np.array(segment['timbre'])
                cosine_similarity = np.dot(reference_timbre, timbre_vector) / (np.linalg.norm(reference_timbre) * np.linalg.norm(timbre_vector))

                if cosine_similarity >= 0.75:
                    # Add this timbre to the current group
                    current_group[key] = segment
                    keys_to_remove.append(key)

            # Remove grouped timbres from temp_analysis
            for key in keys_to_remove:
                del temp_analysis[key]

            if len(current_group) == 1:
                print(f"No similar timbres found for {reference_key}, keeping in analysis_dict")
            else:
            # Store the current group in timbre_groupings
                for key in keys_to_remove:
                    del analysis_dict[key]
                timbre_groupings[f'group_{group_number}'] = current_group
                group_number += 1
        
limit = len(timbre_groupings)

           
i = 1
keys_to_remove = []
while(i <= limit):
    group = timbre_groupings[f"group_{i}"]
    isSinger = True
    isSingerFaultCounter = 0
    for key, segment in group.items():
        pitches = segment['pitches']
        max_pitch = max(pitches)  # Highest pitch value
        sum_of_others = sum(pitches) - max_pitch  # Sum of all other pitch values\
        peak_ratio = max_pitch / sum_of_others
        pitches = np.array(segment['pitches'])
        std_dev = np.std(pitches)
        if(std_dev < 0.2):
            isSingerFaultCounter += 1
        if (peak_ratio < 0.65):
            isSingerFaultCounter += 1
    if (isSingerFaultCounter > 3):
        isSinger = False
    if(isSinger == False):
        keys_to_remove.append(f"group_{i}")
    i += 1

for keys in keys_to_remove:
    del timbre_groupings[keys]



print(timbre_groupings)
        
    




        



    



