import lyricsgenius
import re
import requests, uuid, json

token = "x4hBWY8vSCtAZHgG408ivFbXy5ss4TNa4h8zpo9q0bKuvZsNpl25Z8e4nxhTrVHK"
genius = lyricsgenius.Genius(token, timeout = 15)

artist = genius.search_artist("Drake", max_songs = 1)
song = artist.song("Forever")
lyrics = song.lyrics

def extract_sections(lyrics):
    sections = re.findall(r'\[(.*?)\](.*?)\n(?=\[|$)', lyrics, re.DOTALL)
    return {section[0].strip(): section[1].strip() for section in sections}

# Extracted sections
sections = extract_sections(lyrics)

# Print sections
#for section, content in sections.items():
    #print(f"Section: {section}")
    #print(f"Content: {content}\n")

import re

# Sample lyrics

# Split lyrics into lines
lines = lyrics.split('\n')
#print(lines)

# Initialize variables
current_artist = None
tagged_lyrics = []

# Pattern to match artist tags
artist_pattern = re.compile(r'\[.*: (.+)\]')

# Process each line
for line in lines:
    artist_match = artist_pattern.search(line)
    if artist_match:
        current_artist = artist_match.group(1)
    else:
        if current_artist:
            tagged_lyrics.append({'artist': current_artist, 'lyrics': line})
        else:
            tagged_lyrics.append({'artist': "none", 'lyrics': line})

# Join tagged lyrics back into a single string
print(tagged_lyrics)

# Output the result