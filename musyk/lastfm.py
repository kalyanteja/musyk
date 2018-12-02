import requests

# add a last fm key
LASTFM_API_KEY = '12d5ddb92cc3bfaefd9d016e488d0cd8+dsaewriwer345dsn35kffsd'
LASTFM_TOPTRACKS_API_URL = f'http://ws.audioscrobbler.com/2.0/?method=chart.gettoptracks&api_key={LASTFM_API_KEY}&format=json'
LASTFM_TOPTRACKS_BY_COUNTRY_API_URL = ('http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country={}&api_key={}&format=json')

def top_tracks(country):
    try:
        if country:
            data = requests.get(LASTFM_TOPTRACKS_BY_COUNTRY_API_URL.format(country, LASTFM_API_KEY)).json()
        else:
            data = requests.get(LASTFM_TOPTRACKS_API_URL).json()
    except Exception as exc:
        print(exc)
        data = None
    return data