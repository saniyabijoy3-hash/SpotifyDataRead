import base64
import requests
from dotenv import load_dotenv
import os
import json


load_dotenv('.env')
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

def access_token():
    try:
    
        credentials = f"{CLIENT_ID}:{CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        response = requests.post(url="https://accounts.spotify.com/api/token",                     
           headers={"Authorization": f"Basic {encoded_credentials}"},
           data={"grant_type": "client_credentials"}
        )
        # print(response.json())
        # print(response.json()['access_token'])
        # print("token genarated sucessfully",e)
        
        return response.json()["access_token"]
    except Exception as e:
        print("Error in token generation......",e)


print(access_token())



def get_new_release():
    try:
       token=access_token()
       header={ "Authorization": f"Bearer {token}"}
       Param={"limit": 50}
       response=requests.get("https://api.spotify.com/v1/browse/new-releases",headers=header,params=Param)
       release=[]
       if response.status_code == 200:
        
            data=response.json()
            albums=data["albums"]["items"]
            for album in albums:
                info={
                    "album_name":album["name"],
                    "Release_date":album["release_date"],
                    'album_name': album['name'],
                    'artist_name': album['artists'][0]['name'],
                    'release_date': album['release_date'],
                    'album_type': album['album_type'],
                    'total_tracks': album['total_tracks'],
                    'spotify_url': album['external_urls']['spotify'],
                    'album_image': album['images'][0]['url'] if album['images'] else None

                }
                release.append(info)
            with open("new_release.json","w") as f:
                json.dump(release,f,indent=2)
                print("json data saved  successfully to new_release.json")
    except Exception as e:
        print("Error in lastest release data fetching.......",e)
     
get_new_release()


