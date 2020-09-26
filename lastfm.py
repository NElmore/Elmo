import requests
import json
import requests_cache
import time
import os
from IPython.core.display import clear_output
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('LFM_KEY') 
USER_AGENT = 'nelmobot'
requests_cache.install_cache()

URL = 'http://ws.audioscrobbler.com/2.0/'

def getTopTracksByTag (tag, limit):
    params = {'method' : 'tag.gettoptracks', 'tag' : tag, 'limit' : limit, 'api_key': API_KEY, 'format' : 'json'} 
    result = []
    
    try:
        response = requests.post(URL, data=params, timeout=5).json()
    except requests.exceptions.RequestException as e:
        print (e)
        return None

    if 'error' in response:
        print (response['message'])
        return None
    else:
        for track in response['tracks']['track']:
            temp_list = []
            temp_list.append(track['artist']['name'])
            temp_list.append(track['name'])

            result.append(temp_list)

    return result

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    return text



r = lastfm_get({
    'method': 'chart.gettoptags'
})

def getinfo(track, artist):
    params = {'method' : 'track.getInfo', 'track' : track, 'artist' : artist, 'api_key': API_KEY, 'format' : 'json'}
    response = requests.post(URL, data=params, timeout=5).json()
    
    return response
