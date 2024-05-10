import os
from flask import Flask
from main import get_bitmap_from_url
from spotify import getCurrentSongData

app = Flask(__name__)

@app.route("/", methods=['GET'])
def getImageData():
    songData = getCurrentSongData()

    if songData == {'no-song': ''}:
        return {'no-song': ''}
    
    try:
        albumImageUrl = songData['album']['images'][0]['url']
        bitmapArray = get_bitmap_from_url(albumImageUrl)
        return {'image_data': bitmapArray}
    except:
        return {'no-song': ''}

@app.route("/current-song-data", methods=['GET'])
def currentSongData():
    return getCurrentSongData()

if __name__=="__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host="0.0.0.0",port=5000)