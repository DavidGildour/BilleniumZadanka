import requests
import json

cams_raw = requests.get('http://api.deckchair.com/v1/cameras').content
cams_json = json.loads(cams_raw)['data']

target_cam = ''
for cam in cams_json:
    if 'Mauritius' in cam['title']:
        target_cam = cam
        break
print(target_cam['title'])

id = target_cam['_id']
cam_imgs_raw = requests.get(f'http://api.deckchair.com/v1/camera/{id}/images').content
cam_imgs_json = json.loads(cam_imgs_raw)['data']

img_id = cam_imgs_json[0]['_id']
url = f'http://api.deckchair.com/v1/viewer/image/{img_id}'

with open('test.jpg', 'wb') as f:
    r = requests.get(url)
    f.write(r.content)

print("Image saved to file.")