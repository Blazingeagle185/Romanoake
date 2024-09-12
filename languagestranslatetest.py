from aksharamukha import transliterate
from unidecode import unidecode
import requests
from google.transliteration import transliterate_text
from dotenv import load_dotenv
import os
import requests, uuid, json
import langid
import lyricsgenius
from fuzzywuzzy import fuzz
import re
token = "x4hBWY8vSCtAZHgG408ivFbXy5ss4TNa4h8zpo9q0bKuvZsNpl25Z8e4nxhTrVHK"
genius = lyricsgenius.Genius(token)

load_dotenv()

artist = genius.search_artist("Anirudh Ravichander", max_songs=0, sort="title")
song = artist.song("Kannazhaga")
lyrics = song.lyrics
print(lyrics)


language_scripts = [
    {"code": "ar", "name": "Arabic", "scripts": ["Arab", "Latn"]},
    {"code": "as", "name": "Assamese", "scripts": ["Beng", "Latn"]},
    {"code": "be", "name": "Belarusian", "scripts": ["Cyrl", "Latn"]},
    {"code": "bg", "name": "Bulgarian", "scripts": ["Cyrl", "Latn"]},
    {"code": "bn", "name": "Bangla", "scripts": ["Beng", "Latn"]},
    {"code": "brx", "name": "Bodo", "scripts": ["Deva", "Latn"]},
    {"code": "el", "name": "Greek", "scripts": ["Grek", "Latn"]},
    {"code": "fa", "name": "Persian", "scripts": ["Arab", "Latn"]},
    {"code": "gom", "name": "Konkani", "scripts": ["Deva", "Latn"]},
    {"code": "gu", "name": "Gujarati", "scripts": ["Gujr", "Latn"]},
    {"code": "he", "name": "Hebrew", "scripts": ["Hebr", "Latn"]},
    {"code": "hi", "name": "Hindi", "scripts": ["Deva", "Latn"]},
    {"code": "ja", "name": "Japanese", "scripts": ["Jpan", "Latn"]},
    {"code": "kk", "name": "Kazakh", "scripts": ["Cyrl", "Latn"]},
    {"code": "kn", "name": "Kannada", "scripts": ["Knda", "Latn"]},
    {"code": "ko", "name": "Korean", "scripts": ["Kore", "Latn"]},
    {"code": "ks", "name": "Kashmiri", "scripts": ["Arab", "Latn"]},
    {"code": "ky", "name": "Kyrgyz", "scripts": ["Cyrl", "Latn"]},
    {"code": "mai", "name": "Maithili", "scripts": ["Deva", "Latn"]},
    {"code": "mk", "name": "Macedonian", "scripts": ["Cyrl", "Latn"]},
    {"code": "ml", "name": "Malayalam", "scripts": ["Mlym", "Latn"]},
    {"code": "mn-Cyrl", "name": "Mongolian (Cyrillic)", "scripts": ["Cyrl", "Latn"]},
    {"code": "mni", "name": "Manipuri", "scripts": ["Mtei", "Latn"]},
    {"code": "mr", "name": "Marathi", "scripts": ["Deva", "Latn"]},
    {"code": "ne", "name": "Nepali", "scripts": ["Deva", "Latn"]},
    {"code": "or", "name": "Odia", "scripts": ["Orya", "Latn"]},
    {"code": "pa", "name": "Punjabi", "scripts": ["Guru", "Latn"]},
    {"code": "ru", "name": "Russian", "scripts": ["Cyrl", "Latn"]},
    {"code": "sa", "name": "Sanskrit", "scripts": ["Deva", "Latn"]},
    {"code": "sd", "name": "Sindhi", "scripts": ["Arab", "Latn"]},
    {"code": "si", "name": "Sinhala", "scripts": ["Sinh", "Latn"]},
    {"code": "sr-Cyrl", "name": "Serbian (Cyrillic)", "scripts": ["Cyrl"]},
    {"code": "sr-Latn", "name": "Serbian (Latin)", "scripts": ["Latn"]},
    {"code": "ta", "name": "Tamil", "scripts": ["Taml", "Latn"]},
    {"code": "te", "name": "Telugu", "scripts": ["Telu", "Latn"]},
    {"code": "tg", "name": "Tajik", "scripts": ["Cyrl", "Latn"]},
    {"code": "th", "name": "Thai", "scripts": ["Thai", "Latn"]},
    {"code": "tt", "name": "Tatar", "scripts": ["Cyrl", "Latn"]},
    {"code": "uk", "name": "Ukrainian", "scripts": ["Cyrl", "Latn"]},
    {"code": "ur", "name": "Urdu", "scripts": ["Arab", "Latn"]},
    {"code": "zh-Hans", "name": "Chinese Simplified", "scripts": ["Hans", "Latn", "Hant"]},
    {"code": "zh-Hant", "name": "Chinese Traditional", "scripts": ["Hant", "Latn", "Hans"]}
]
key = os.getenv("AZURE_KEY")
endpoint = "https://api.cognitive.microsofttranslator.com"
endpoint2 = "https://api.cognitive.microsofttranslator.com/languages?api-version=3.0"

location = "eastus"
path = '/transliterate'
constructed_url = endpoint + path

params = {
    'api-version': '3.0',
    'language': 'ta',
    'fromScript': 'Taml',
    'toScript': 'Latn'
}

headers = {
    'Ocp-Apim-Subscription-Key': key,
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}
'''லைஃப்ல வைஃப் வந்திட்டா
டைட்டாதான் இருக்கணும்
வெயிட்டானா பொண்ணை பார்த்தாலும்
ரைட்டாதான் நடக்கணும்
வீட்டுக்கு ஃபிரெண்ட்ஸ் எல்லாம் வந்தா
கெஸ்டாதான் நடத்தனும்
உன்மேல தப்பில்லடியும்
சைலன்டா இருக்கணும்
ல ல ல ல ல ல ல ல
ல ல ல ல ல ல ல ல
கமான் கேர்ல்ஸ்
ல ல ல ல ல ல ல ல
ல ல ல ல ல ல ல ல
♪
ஒன்னோட ஒண்ணு சேர்ந்து ரெண்டாக ஆயாச்சு
ஃபிரண்ட் இப்ப கேர்ல் ஃபிரண்ட் ஆச்சு.
ஆணோட பொண்ணு சேர்ந்து மாப்ளை ஆயாச்சு
டைடானிக் கப்பல் ஆச்சு .
ஜனனி கண்மணி, என் உரியர் நீயடி
போர் அடிக்காம நீ ஆடுடி
ல ல ல ல ல ல ல ல
ல ல ல ல ல ல ல ல
கமான் கேர்ல்ஸ்
ல ல ல ல ல ல ல ல
ல ல ல ல ல ல ல ல
♪
கமான் கேர்ல்ஸ்
'''
params1 = {
    'api-version': '3.0'
}
body = [
    {"Text":"கொலவெரி"}
]
endpoint3 = "https://api.cognitive.microsofttranslator.com/detect?api-version=3.0"
text = "எங்கேயோ பார்க்கிறாய் என்னென்ன சொல்கிறாய்"
words = text.split()
scripts = []
request = requests.post(endpoint3, params=params1, headers=headers, json = body)
response = request.json()
lang = response.get("language")
i = 0
limit = len(words)
isMultipleScripts = False
while(i < limit):
    script = transliterate.auto_detect(words[i])
    scripts.append(script)    
    j = 0
    while(j <= i):
        currentscript = scripts[j]
        if (currentscript != script and script != "HK"):
            isMultipleScripts = True
        j += 1
    i+= 1


print(scripts)
transliterate_phrases = []
isMultipleScripts = True
if(isMultipleScripts):
    j = 0
    while(j < limit):
        print(words[j])
        lang, confidence = langid.classify(words[j])
        for language in language_scripts:
            code = language['code']
            if(code == lang):
                script = language['scripts'][0]
                print(script)
                lang_param = language['name']
                print(lang_param)
                break
        if(lang != "en"):
            params = {
                'api-version': '3.0',
                'language': lang,
                'fromScript': script,
                'toScript': 'Latn'
            }
            print(params)
            body = [{"text": words[j]}]
            try:
                request = requests.post(constructed_url, params=params, headers=headers, json=body)
                response = request.json()
                params = {
                    'api-version': '3.0',
                    'language': lang,
                    'fromScript': "Latn",
                    'toScript': script
                }
                print(params)
                body = [{"text": response[0]["text"]}]
                request1 = requests.post(constructed_url, params=params, headers=headers, json=body)
                response1 = request1.json()
                print(response1[0]["text"])
                #text = response.get("text")
                transliterate_phrases.append(response[0]["text"])
            except:
                text = transliterate.process("autodetect", "HK", words[j])
                transliterate_phrases.append(text)
        else:
            transliterate_phrases.append(words[j])
        j+=1
        print(transliterate_phrases)
    print(transliterate_phrases)

complete_lyrics = ' '.join(transliterate_phrases)
print(complete_lyrics)


j = 0
while(j < limit): 
    lang, confidence = langid.classify(words[j])
    for language in language_scripts:
        code = language['code']
        if(code == lang):
            script = language['scripts'][0]
            print(script)
            lang_param = language['name']
            print(lang_param)
            break
    i = 0
    best_match = None
    highest_ratio = 0
    for line in lyrics.split('\n'):
        ratio = fuzz.ratio(line, complete_lyrics)
        if ratio > highest_ratio:
            highest_ratio = ratio
            best_match = line
    print(highest_ratio)
    best_match = best_match.split()
    ["fasdfdasf", "fjjasdfkjasklfj"]
    i = 0    
    highest_ratio = 0
    match = None
    for word in best_match:
        ratio = fuzz.ratio(best_match[i], transliterate_phrases[j])
        if ratio > highest_ratio:
            highest_ratio = ratio
            match = best_match[i]
        i+=1
    print(highest_ratio)       
    params = {
        'api-version': '3.0',
        'language': lang,
        'fromScript': "Latn",
        'toScript': script
    }
    if(lang != "en"):
        body = [{"text": transliterate_phrases[j]}]
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        trans = request.json()
        print(best_match)
        print(words[j])
        print(transliterate_phrases[j])
        print(match)
        ratio_trans = fuzz.ratio(words[j], trans[0]["text"])
        print(trans[0]["text"])
        #சைலண்டா வந்தா
        #நீயடி வந்தா
        #உரியர் ஃப்ரென்ட்ஸ்
        body = [{"text": match}]
        request = requests.post(constructed_url, params=params, headers=headers, json=body)
        genius = request.json()
        print(genius[0]["text"])
        ratio_genius = fuzz.ratio(words[j], genius[0]["text"])
        if (ratio_genius > ratio_trans):
            transliterate_phrases[j] = match
    j+=1
print(best_match)
print(transliterate_phrases)
