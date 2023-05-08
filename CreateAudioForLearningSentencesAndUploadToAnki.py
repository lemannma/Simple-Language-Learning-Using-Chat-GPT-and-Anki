"""
Created on Sat Apr 15 15:18:59 2023

@authors: Dr. Olga Lehmann and Matthias Lehmann
"""

from gtts import gTTS
import json
import urllib.request

path = '{your List}.txt'
language_code = 'fr' #fr for french 
deckName = "{your Anki Deck}"
#Hint: if you store files in the collection.media folder you can directly reference them in fields section of the note
urlForAudioMedia = "{link to your Anki collection.media folder}" 


def request(action, **params):
    return {'action': action, 'params': params, 'version': 6}

def invoke(action, **params):
    requestJson = json.dumps(request(action, **params)).encode('utf-8')
    response = json.load(urllib.request.urlopen(urllib.request.Request('http://localhost:8765', requestJson)))
    if len(response) != 2:
        raise Exception('response has an unexpected number of fields')
    if 'error' not in response:
        raise Exception('response is missing required error field')
    if 'result' not in response:
        raise Exception('response is missing required result field')
    if response['error'] is not None:
        raise Exception(response['error'])
    return response['result']

def addNote(front, back, filename):     
    audioLink = "[sound:"+filename+"]"    
    return invoke('addNote',    
        note={
            "deckName": deckName,
            #Hint: modles are individualy difined by Anki users
            "modelName": "Einfach (beide Richtungen)",
            #Hint: fields are individualy difined by Anki users
            "fields": {
                #text plus direct reference to audio file
                "Vorderseite": front + audioLink,
                "Rückseite": back
            },
            "options": {
                "allowDuplicate": False,
            "duplicateScope": "deck",
            "duplicateScopeOptions": { "deckName": "Test", "checkChildren": False }
            },
            "tags": ["#Export"]
        }
    )

def createFlashcardsWithAudio(line):
    parts = line.split(":")
    front = parts[0].strip()
    back = parts[1].strip()
    tts = gTTS(text=front, lang=language_code)
    filename = front.replace(" ", "_") + ".mp3"
    filename = filename.replace("/", "_")
    #storage of audio file in collection.media folder 
    tts.save(urlForAudioMedia + filename)
    addNote(front, back, filename) 

#load remaining learning content
content = []

with open(path, mode='r') as f:
    content = f.readlines()
     
content_to_load = content[:10]
remaining_content = content[10:]
 
for line in content_to_load:
   createFlashcardsWithAudio(line)

#save remaining sentences
with open(path, mode='w') as f:
    for item in remaining_content:
        f.write("%s" % item)


