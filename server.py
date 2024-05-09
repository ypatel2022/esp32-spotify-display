from flask import Flask
from main import get_bitmap_from_url

app = Flask(__name__)

@app.route("/")
def getImageData():
    bmp = get_bitmap_from_url('')
    return {'image_data': bmp}

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
scope = "user-read-currently-playing"

@app.route('/currently-playing')
def currentlyPlaying():
    return ''