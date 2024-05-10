import os
import requests
import base64

from dotenv import load_dotenv
load_dotenv()

def getAccessToken():
    url = 'https://accounts.spotify.com/api/token'

    REFRESH_TOKEN = os.environ.get("SPOTIFY_REFRESH_TOKEN")
    CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")

    auth_client = CLIENT_ID + ":" + CLIENT_SECRET
    auth_encode = 'Basic ' + base64.b64encode(auth_client.encode()).decode()

    headers = {'Authorization': auth_encode}


    data = {'grant_type' : 'refresh_token','refresh_token' : REFRESH_TOKEN}

    response = requests.post(url=url, data=data, headers=headers)

    if(response.status_code == 200): #checks if request was valid
        # print("The request to went through we got a status 200; Spotify token refreshed")

        response_json = response.json()

        new_expire = response_json['expires_in']
        # print("the time left on new token is: "+ str(new_expire / 60) + "min")

        return response_json["access_token"]
    
    # not 200 code    
    print("ERROR! The response we got was: "+ str(response))
    return None


def getCurrentSongData():
    url = 'https://api.spotify.com/v1/me/player/currently-playing'

    accessToken = getAccessToken()

    header = {'Authorization': f'Bearer {accessToken}'}

    response = requests.get(url=url, headers=header)

    if (response.status_code == 200):
        res_json = response.json()
        # print(res_json)
        return res_json['item']
    
    return {'no-song': ''}


if __name__ == '__main__':
    getCurrentAlbumUrl()