import requests

ALL_COUNTRIES_APP_URL = 'https://restcountries.eu/rest/v2/all'


def all_countries():
    try:
        data = requests.get(ALL_COUNTRIES_APP_URL).json()
    except Exception as exc:
        print(exc)
        data = None
    return data