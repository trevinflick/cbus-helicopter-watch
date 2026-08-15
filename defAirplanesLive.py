import time
import requests

def pull_airplaneslive(icao):
    time.sleep(2)  # avoid 429s when polling multiple ICAOs in sequence
    url = "https://opendata.adsb.fi/api/v2/hex/" + icao
    headers = {"User-Agent": "plane-notify (https://github.com/Jxck-S/plane-notify)"}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        data = response.json()
        if "msg" in data.keys() and data['msg'] != "No error":
            raise ValueError("Error from airplanes.live: msg = ", data['msg'])
        return data
    except Exception as e:
        print('Error calling airplanes.live', e)
    return None
