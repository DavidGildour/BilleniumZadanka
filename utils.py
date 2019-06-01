import datetime
import requests
import json

from re import search


def cam_fetcher(cam_url: str):
    cams = request_to_json('http://api.deckchair.com/v1/cameras')
    html = requests.get(cam_url).text
    exp = r'content="(.+) - HD Webcam"'

    cam_name = search(exp, html).group(1)

    for cam in cams:
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
