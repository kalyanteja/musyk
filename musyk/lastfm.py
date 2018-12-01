import requests

LASTFM_API_KEY = '12d5ddb92cc3bfaefd9d016e488d0cd8'
LASTFM_API_URL = f'http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key={LASTFM_API_KEY}&format=json'
def top_tracks():
    try:
        print(LASTFM_API_URL)
        data = requests.get(LASTFM_API_URL).json()
    except Exception as exc:
        print(exc)
        data = None
    return data