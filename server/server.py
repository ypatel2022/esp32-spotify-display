import os
from flask import Flask
from main import get_bitmap_from_url
from multiprocessing import Value

counter = Value('i', 0)
app = Flask(__name__)

@app.route("/", methods=['GET'])
def getImageData():

    with counter.get_lock():
        counter.value += 1
        i = counter.value

    bmp = {}
    if i % 5 == 0:
        bmp = get_bitmap_from_url('https://i.scdn.co/image/ab67616d00001e02715973050587fe3c93033aad')
    elif i % 5 == 1:
        bmp = get_bitmap_from_url('https://i.scdn.co/image/ab67616d00001e021dacfbc31cc873d132958af9')
    elif i % 5 == 2:
        bmp = get_bitmap_from_url('https://i.scdn.co/image/ab67616d00001e0226f7f19c7f0381e56156c94a')
    elif i % 5 == 4:
        bmp = get_bitmap_from_url('https://i.scdn.co/image/ab67616d00001e0242281601a5a3f882ea77741e')
    else:
        bmp = get_bitmap_from_url('https://i.scdn.co/image/ab67616d00001e02e9b58064013b722f09296b3e')
        
    return {'image_data': bmp}

@app.route("/test", methods=['GET'])
def testRoute():
    return {'test': 'test'}

if __name__=="__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True,host="0.0.0.0",port=5000)