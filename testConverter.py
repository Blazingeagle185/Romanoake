def process():
    import os, re, sys, spotipy, itertools, json, requests, base64, linecache, bs4, time, pyperclip, pprint, datetime, shutil, platform, subprocess
    import spotipy.util as util
    import requests
    import logging
    import string
    from spotipy import oauth2
    import spotipy
    from spotipy import client
    from os import path
    from spotipy.oauth2 import SpotifyOAuth
    from bs4 import BeautifulSoup
    from pathlib import Path #using this module to solve difference path syntax between Mac OS and Windows
    from dotenv import load_dotenv
    from flask import Flask, request, jsonify, send_from_directory, Blueprint
    from flask_cors import CORS

    load_dotenv()


    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv("CLIENT_ID"),
                                                client_secret=os.getenv("CLIENT_SECRET"),
                                                redirect_uri="http://localhost:1234"))
    # MAKE SURE THESE ARE CORRECT
    CLIENT_ID = os.getenv("CLIENT_ID")
    CLIENT_SECRET = os.getenv("CLIENT_SECRET")
    REDIRECT_URI =  'http://localhost:1234'
    authorization = "Bearer BQDoV6EnNEvD4y7L7eAhIHEowrobbKE3-Ca5SnmqfuC6KlZ9jfClk4LUB4e5coJTSxYQIutYgewlJvyQ657cKF5UtAGophZll9jGdOGwbAyjj4Xnbj9HW2A3atPkc0t84gjo6SLpIjqpNYDZxcq5hIGLwttnIfLl7NTe9KapkO83NuYP1VKx6F9O94K2uSMIShjGXdXGtBYEdaSl9P76BAGfZcOuW-dRY9bFHv3OzvXCiKEYvOlCWXHu_0sWy-3fjQk2_3ONFtRXhJ1S4Kbx-6a2KLu8xYDrEKCdsksp-xGWkwolBTkX6hI05n9905b_aSmcrTpicmF-_OUGnfRJJDUMO27yqwMdOg"
    os.environ['SPOTIPY_CLIENT_ID']  = CLIENT_ID
    os.environ['SPOTIPY_CLIENT_SECRET'] = CLIENT_SECRET
    os.environ['SPOTIPY_REDIRECT_URI'] = REDIRECT_URI
    scope = "user-read-currently-playing"
    # spotipy authentication to see currently playing song
    sp = spotipy.Spotify(auth_manager = SpotifyOAuth(scope = scope))
    current_track = sp.current_user_playing_track()


    def replace_line(database, line_num, text):
        lines = open(database, 'r').readlines()
        lines[line_num] = text
        out = open(database, 'w')
        out.writelines(lines)
        out.close()

    #for opening folder in various operating system explorers
    def open_file(path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path]) 

    def sanitize_filename(filename):
        # Replace invalid characters with underscores
        valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
        return ''.join(c if c in valid_chars else '_' for c in filename)

    #see if song is playing
    if current_track == None:
        print("No song detected, make sure you're actively playing a song!")
        os._exit(0)
    '''
    song_uri_link = current_track.get("uri").replace('spotify:track:','')
    song_name = sanitize_filename(current_track.get("name"))
    cover_link = current_track.get("album").get("images")[0].get("url")
    release_date = current_track.get("album").get("release_date")
    album_name = sanitize_filename(current_track.get("album").get("name"))
    artist_name = sanitize_filename(current_track.get("album").get("artists")[0].get("name"))
    track_number = current_track.get("track_number")
    album_uri_link = current_track.get("album").get("uri")
    '''

    song_uri_link = current_track.get("item").get("uri").replace('spotify:track:','')
    song_name = current_track.get("item").get("name")
    cover_link = current_track.get("item").get("album").get("images")[0].get("url")
    release_date = current_track.get("item").get("album").get("release_date")
    album_name = current_track.get("item").get("album").get("name")
    artist_name = current_track.get("item").get("album").get("artists")[0].get("name")
    track_number = current_track.get("item").get("track_number")
    album_uri_link = current_track.get("item").get("album").get("uri")

    # generate lyrics link
    original_link = cover_link
    a = cover_link
    a = a.replace("/", "%2F")
    a = a.replace(":", "%3A")
    cover_link = a
    link_start = "https://spclient.wg.spotify.com/color-lyrics/v2/track/"
    lyrics_url = (link_start + song_uri_link + "/image/" + cover_link + "?format=json&vocalRemoval=false&market=from_token")
    lyrics_url_no_access = (link_start + song_uri_link + "/image/" + cover_link)

    print("Success! Song detected! \n")
    print("Song: ", song_name)
    print("Album name:", album_name)
    print("Artist name:", artist_name)
    print("Track number: ", track_number)
    print("Release date: ", release_date)
    print("Album cover URL:", original_link)
    print("Track URI:", song_uri_link)
    print("Album URI:", album_uri_link)
    print("Lyric URL:", lyrics_url, "\n")

    # getting release year for album
    release_date = release_date.replace('-', '/')
    release_year = release_date[:4]

    # creates directory
    artist = artist_name
    album = (album_name + " (" + release_year + ")")
    song = song_name
    song = sanitize_filename(song)
    track_number = track_number
    lyrics = "Lyrics"
    host_dir = os.getcwd()
    # print("Host Directory: \n" + host_dir)

    album_info = sp.album_tracks(album_uri_link)

    # saves currently playing album info to txt file
    result = json.dumps(album_info)
    z = open("album_info.txt", "w")
    z.write(result)
    z.close()
    album_database = "album_info.txt"
    with open('album_info.txt', 'r') as handle:
        parsed = json.load(handle)
        parsed2 = (json.dumps(parsed, indent=1, sort_keys=True))
    with open('album_info.txt', 'w') as file: # line breaks
        file.write(parsed2)
        file.close()

    #reading for short line removal
    with open('album_info.txt', 'r')  as f:
        lines = f.readlines()
    # Removes region codes by removing all short lines
    filtered_lines = [line for line in lines if len(line) > 10]
    # writing out file w no 2-character country codes
    with open('filtered_album_info.txt', 'w') as f:
        for line in filtered_lines:
            f.write(line)
    os.remove("album_info.txt")
    os.rename('filtered_album_info.txt', "album_info.txt")
    #if needed, commewnt below line out for album_info saved to txt
    os.remove("album_info.txt")
        
    #creates lyrics folder
    lyrics = sanitize_filename(lyrics)
    if os.path.isdir(lyrics):
        os.chdir(lyrics)
        lyricdir = os.getcwd()
    else:
        os.mkdir(lyrics)
        os.chdir(lyrics)

    artist = sanitize_filename(artist)
    #creates artist folder
    if os.path.isdir(artist):
        os.chdir(artist)
        artistdir = os.getcwd()
    else:
        os.mkdir(artist)
        os.chdir(artist)
        artistdir = os.getcwd()

    album = sanitize_filename(album)
    #creates album folder
    if os.path.isdir(album):
        os.chdir(album)
        albumdir = os.getcwd()
    else:
        os.mkdir(album)
        os.chdir(album)
        albumdir = os.getcwd()

    os.chdir(host_dir)

    #set up variables for moving lyric and setting up cover.jpg location
    host_folder = host_dir
    lyrics = "Lyrics"
    artist_name = artist_name
    albumdir = albumdir
    song = song
    cover = lyrics_url
    originallyricsfile = (Path(host_folder)/"output.lrc")
    movedlyricsfile = (Path(albumdir)/(str(track_number) + ". " + str(song) + ".lrc"))
    movedcoverjpg = (Path(albumdir)/"cover.jpg")

    #checks if cover exists, if not it downloads
    os.chdir(albumdir)
    try:
        f = open(movedcoverjpg)
        print("Cover already downloaded, skipping download.")
        f.close()
    except IOError:
        print("No cover.jpg detected, downloading now")
        cover =requests.get(original_link).content
        f = open(movedcoverjpg,'wb')
        f.write(cover)
        f.close()
        print("Cover downloaded!")

    os.chdir(host_dir)
    #checks if lyric exists, if not it downloads
    try:
        f = open(movedlyricsfile)
        print("Lyric already downloaded, skipping download. Enjoy!")
        f.close()
        open_file(albumdir)
        os.remove("currentsong.txt")
        quit()

    except IOError:
        print("No lyric detected, downloading now")

    headers = {
        'Host': 'spclient.wg.spotify.com',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'accept-language': 'en',
        'sec-ch-ua-mobile': '?0',
        'app-platform': 'WebPlayer',
        'authorization': authorization,
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
        'accept': 'application/json',
        'spotify-app-version': '1.1.98.597.g7f2ab0d4',
        'sec-ch-ua-platform': '"macOS"',
        'origin': 'https://open.spotify.com',
        'sec-fetch-site': 'same-site',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://open.spotify.com/',
    }
    
    params = {
        'format': 'json',
        'vocalRemoval': 'false',
        'market': 'from_token',
    }
    response = requests.get(lyrics_url, params=params, headers=headers)
    response.encoding = 'utf-8'
    lyricdata=response.text
    #print(lyricdata)
    z = open("lyrics.txt", "w", encoding="utf-8")
    z.write(lyricdata)
    z.close()
    print("Successfully saved page text, will verify...")

    # coding:utf-8
    import os, re, sys, itertools, json, requests, base64, linecache, time, requests, bs4, time, pyperclip, pprint, shutil, platform, subprocess
    import string
    from pathlib import Path #using this module to solve difference path syntax between Mac OS and Windows



    host_folder = host_dir #get work path
    os.chdir(host_folder) #change path to work path
    lyrics_url = lyrics_url

    # Read in the jumbled Spotify lyric text
    with open('lyrics.txt', 'r',encoding='UTF-8') as file :
        filedata = file.read()
        fullstring = filedata
    substring_403 = "HTTP ERROR 403"
    substring_401 = '"status": 401,'
    substring_success = "lyrics"

    print("Searching for valid lyrics...")
    # exception for songs with no lyrics
    if substring_403 in fullstring:
        os.remove("lyrics.txt")
        print("Lyrics not available for this song, sorry!")
        if len(os.listdir(albumdir)) == 0: # Check if the album folder is empty
            shutil.rmtree(albumdir) # If so, delete it
            if len(os.listdir(artistdir)) == 0: # Check if the artist folder is empty
                shutil.rmtree(artistdir) # If so, delete it
                quit()
    # exception with no token, just redownloads it based on lyrics_url
    elif substring_401 in fullstring:
        print("Error, token has been expired, please open the browser to get a new one and restart the program")
        os._exit(0)
        
    #exception for successful lyric grab
    elif substring_success in fullstring:
        print("Lyric grab was success, converting now...")
        with open('lyrics.txt', 'r', encoding = 'utf-8') as file :
            filedata = file.read()
            fullstring = filedata

    # Remove some of the Spotify formatting
    filedata = filedata.replace('},', '} \n')
    filedata = filedata.replace('{"lyrics":{"syncType":"LINE_SYNCED","lines":[', '')
    filedata = filedata.replace('\\u0027', '\'')
    filedata = filedata.replace('{"startTimeMs":"', '[')
    filedata = filedata.replace(',"syllables":[]} ', '')
    filedata = filedata.replace('","words":', ']')
    filedata = filedata.replace('"', '')
    filedata = filedata.replace('hasVocalRemoval:false}', '')
    filedata = filedata.replace(']', '] ')
    filedata = filedata.replace('\\', '*')
    filedata = filedata.replace(',syllables:[] ,endTimeMs:0}', '')

    # Write the file out
    with open('lyricsfixed.lrc', 'w', encoding = 'utf-8') as file:
        file.write(filedata)

    # remove leftover shit from Spotify that doesnt apply to lrc files
    with open("lyricsfixed.lrc", "r", encoding = 'utf-8') as f:
        lines = f.readlines() 
    with open("lyricsfixed.lrc", "w", encoding = 'utf-8') as new_f:
        for line in lines:
            if not line.startswith("colors:{background"):
                new_f.write(line)

    # removes last line of gibberish
    import os, sys, re
    readFile = open("lyricsfixed.lrc", encoding = 'utf-8')
    lines = readFile.readlines()
    readFile.close()
    w = open("lyricsfixed.lrc",'w', encoding = 'utf-8')
    w.writelines([item for item in lines[:-1]])
    w.close()

    with open('lyricsfixed.lrc', 'r', encoding = 'utf-8') as file :
        filedata = file.read()
    # I keep initializing it the same way and just reassigning the filedata string because i am idiot brain (stop doing this!)
    test_str = filedata

    # Extracts all regions in ms into a string
    # Using regex which i do not get at all
    res = re.findall(r"\[\s*\+?(-?\d+)\s*\]", test_str)
    # saving timings to timings.txt
    file = open("timings.txt", "w", encoding = 'utf-8')

    formatted_times = [] #timing conversion
    for time in res:
        millis = int((int(time) % 1000) / 10)
        secs = int(int(time) / 1000)
        mins = int(secs / 60)
        secs = secs % 60
        formatted_times.append(f"{mins}:{secs}.{millis}")

    text = '] \n'.join(formatted_times) # line breaks
    file.write(text)
    file.close()

    # Read in the file
    with open('timings.txt', 'r', encoding = 'utf-8') as file :
        filedata = file.read()

    # Bad logic to add brackets and keep timing scheme consistent because im dumb
    filedata = filedata.replace('0:', '[00:')
    filedata = filedata.replace('1:', '[01:')
    filedata = filedata.replace('2:', '[02:')
    filedata = filedata.replace('3:', '[03:')
    filedata = filedata.replace('4:', '[04:')
    filedata = filedata.replace('5:', '[05:')
    filedata = filedata.replace('6:', '[06:')
    filedata = filedata.replace('7:', '[07:')
    filedata = filedata.replace('8:', '[08:')
    filedata = filedata.replace('9:', '[09:')
    filedata = filedata.replace(':0.', ':00.')
    filedata = filedata.replace(':1.', ':01.')
    filedata = filedata.replace(':2.', ':02.')
    filedata = filedata.replace(':3.', ':03.')
    filedata = filedata.replace(':4.', ':04.')
    filedata = filedata.replace(':5.', ':05.')
    filedata = filedata.replace(':6.', ':06.')
    filedata = filedata.replace(':7.', ':07.')
    filedata = filedata.replace(':8.', ':08.')
    filedata = filedata.replace(':9.', ':09.')
    filedata = filedata.replace('.9]', '.90]')
    filedata = filedata.replace('.8]', '.80]')
    filedata = filedata.replace('.7]', '.70]')
    filedata = filedata.replace('.6]', '.60]')
    filedata = filedata.replace('.5]', '.50]')
    filedata = filedata.replace('.4]', '.40]')
    filedata = filedata.replace('.3]', '.30]')
    filedata = filedata.replace('.2]', '.20]')
    filedata = filedata.replace('.1]', '.10]')
    filedata = filedata.replace('.0]', '.00]')
    with open('timingsfixed.txt', 'w', encoding = 'utf-8') as file:
        file.write(filedata)

    with open('timingsfixed.txt', 'r', encoding = 'utf-8') as file :
        filedata = file.read()
    filedata = filedata.replace('1 ', '1]')
    filedata = filedata.replace('2 ', '2]')
    filedata = filedata.replace('3 ', '3]')
    filedata = filedata.replace('4 ', '4]')
    filedata = filedata.replace('5 ', '5]')
    filedata = filedata.replace('6 ', '6]')
    filedata = filedata.replace('7 ', '7]')
    filedata = filedata.replace('8 ', '8')
    filedata = filedata.replace('9 ', '9]')

    # bad file editing to catch the last bracket not applying
    s1 = filedata
    s2 = "]"
    filedatawithlastbracket = (s1 + s2) 

    with open('timingsfixed.txt', 'w', encoding = 'utf-8') as file:
        file.write(filedatawithlastbracket)

    os.remove("timings.txt")
    os.rename('timingsfixed.txt', 'timingsfixed.lrc')

    with open('lyricsfixed.lrc', 'r', encoding = 'utf-8') as file :
        filedata = file.read()
    # doing what i did earlier, very janky and very backwards, to extract whats *not* in the brackets to get the words to apply the new times to
    test_str = filedata
    a_string = test_str
    modified_string = re.sub(r"\[\s*\+?(-?\d+)\s*\]", "", a_string) # just the words from the song, prints without timecodes
    # print(modified_string)

    with open('lyricstimingsremoved.txt', 'w', encoding = 'utf-8') as file:
        file.write(modified_string)

    from itertools import zip_longest
    with open('timingsfixed.lrc', 'r', encoding = 'utf-8') as file :
        filedata = file.read()
    with open('lyricstimingsremoved.txt', 'r', encoding = 'utf-8') as file1:
        test_str = file1.read()
    #combines new timing and lyric files, A/B/A/B style, no AA/BB
    with open('timingsfixed.lrc', 'r', encoding = 'utf-8') as src1, open('lyricstimingsremoved.txt', 'r', encoding = 'utf-8') as src2, open('output.lrc', 'w', encoding = 'utf-8') as dst:
        for line_from_first, line_from_second in itertools.zip_longest(src1, src2):
            if line_from_first is not None:
                dst.write(line_from_first)
            if line_from_second is not None:
                dst.write(line_from_second)

    with open('output.lrc', 'r', encoding = 'utf-8') as file :
        filedata = file.read()
    filedata = filedata.replace('   ', '')
    with open('output.lrc', 'w', encoding = 'utf-8') as file:
        file.write(filedata)
    #combines into one line where line breaks can be added
    with open('output.lrc', encoding = 'utf-8') as f:
        all_lines = f.readlines()
        all_lines = [x.strip() for x in all_lines if x.strip()]
        two_lines = " ".join(x for x in all_lines[:2])
        lines_left = " ".join(x for x in all_lines[2:])

    oneline = (two_lines + lines_left)
    #everything put into one line, needed for line breaks

    # Breaks multiple lines colliding making LRC file unreadable
    oneline = oneline.replace(' [', '\n[')
    oneline = oneline.replace('\\', '')
    oneline = oneline.replace(')[', ')\n[')
    oneline = oneline.replace('.[', '.\n[')
    oneline = oneline.replace('![', '!\n[')
    oneline = oneline.replace('?[', '?\n[')
    oneline = oneline.replace('a[', 'a\n[')
    oneline = oneline.replace('b[', 'b\n[')
    oneline = oneline.replace('c[', 'c\n[')
    oneline = oneline.replace('d[', 'd\n[')
    oneline = oneline.replace('e[', 'e\n[')
    oneline = oneline.replace('f[', 'f\n[')
    oneline = oneline.replace('g[', 'g\n[')
    oneline = oneline.replace('h[', 'h\n[')
    oneline = oneline.replace('i[', 'i\n[')
    oneline = oneline.replace('j[', 'j\n[')
    oneline = oneline.replace('k[', 'k\n[')
    oneline = oneline.replace('l[', 'l\n[')
    oneline = oneline.replace('m[', 'm\n[')
    oneline = oneline.replace('n[', 'n\n[')
    oneline = oneline.replace('o[', 'o\n[')
    oneline = oneline.replace('p[', 'p\n[')
    oneline = oneline.replace('q[', 'q\n[')
    oneline = oneline.replace('r[', 'r\n[')
    oneline = oneline.replace('s[', 's\n[')
    oneline = oneline.replace('t[', 't\n[')
    oneline = oneline.replace('u[', 'u\n[')
    oneline = oneline.replace('v[', 'v\n[')
    oneline = oneline.replace('w[', 'w\n[')
    oneline = oneline.replace('x[', 'x\n[')
    oneline = oneline.replace('y[', 'y\n[')
    oneline = oneline.replace('z[', 'z\n[')
    oneline = oneline.replace('[00:00.00] {lyrics:{syncType:UNSYNCED,lines:[ ', '')
    oneline = oneline.replace('[00:00.00] ', '')
    oneline = oneline.replace('[00:00.0] ', '')
    oneline = oneline.replace('.9]', '.90]')
    oneline = oneline.replace('.8]', '.80]')
    oneline = oneline.replace('.7]', '.70]')
    oneline = oneline.replace('.6]', '.60]')
    oneline = oneline.replace('.5]', '.50]')
    oneline = oneline.replace('.4]', '.40]')
    oneline = oneline.replace('.3]', '.30]')
    oneline = oneline.replace('.2]', '.20]')
    oneline = oneline.replace('.1]', '.10]')
    oneline = oneline.replace('.0]', '.00]')

    #writing final lines
    with open('output.lrc', 'w', encoding = 'utf-8') as file:
        file.write(oneline)
        print("Conversion complete!")

    #remove leftover files
    os.remove("lyricsfixed.lrc")
    os.remove("lyricstimingsremoved.txt")
    os.remove("timingsfixed.lrc")
    os.remove("lyrics.txt")

    #set up variables for moving lyric and setting up cover.jpg location
    host_folder =host_dir
    lyrics = "Lyrics"
    artist_name = artist_name
    albumdir = albumdir
    song = song_name
    cover = lyrics_url
    originallyricsfile = (Path(host_folder)/"output.lrc")
    movedlyricsfile = (Path(albumdir)/(str(track_number) + ". " + str(song) + ".lrc"))
    movedcoverjpg = (Path(albumdir)/"cover.jpg")

    #prints folder where lyric went
    print("\n")
    print("Moved lyric to:")
    print(movedlyricsfile, "\n")
    newPath = shutil.move(originallyricsfile, movedlyricsfile)
    '''
    def open_file(path):
        if platform.system() == "Windows":
            os.startfile(path)
        elif platform.system() == "Darwin":
            subprocess.Popen(["open", path])
        else:
            subprocess.Popen(["xdg-open", path])
            
    open_file(albumdir)
    '''
if __name__ == "__main__":
    process()