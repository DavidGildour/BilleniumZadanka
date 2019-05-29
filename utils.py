import datetime
import requests
import json


def cam_fetcher(cam_name: str):
    cams_raw = requests.get('http://api.deckchair.com/v1/cameras').content
    cams_json = json.loads(cams_raw)['data']

    for cam in cams_json:
        if cam_name in cam['title']:
            return cam
    return None


def request_to_json(url: str):
    req = requests.get(url).content

    return json.loads(req)['data']


def convert_to_datetime(timestamp: str):
    timestamp = timestamp.split('T')
    dt_str, tm_str = timestamp[0], timestamp[1][:-6]
    dt_arr = list(map(int, dt_str.split('-')))
    tm_arr = list(map(int, tm_str.split(':')))

    return datetime.datetime(*dt_arr, *tm_arr)
