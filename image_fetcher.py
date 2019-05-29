import requests
import time
import datetime

from utils import cam_fetcher, convert_to_datetime, request_to_json


class ImageFetcher:
    def __init__(self, cam: str):
        self.cam = cam_fetcher(cam)
        if self.cam:
            self.cam_found = True
            self.cam_name = self.cam['title']
            self.cam_id = self.cam['_id']
            # checking timezone difference
            _, cam_date = self.fetch_latest()
            cam_h = cam_date.hour
            local_h = datetime.datetime.now().hour
            tzdiff = datetime.timedelta(hours=(local_h - cam_h))
            datetime.timezone(tzdiff)
            print(f"Timezone diff: {tzdiff}.")
        else:
            self.cam_found = False

    def fetch_latest(self):
        cam_imgs = request_to_json(f'http://api.deckchair.com/v1/camera/{self.cam_id}/images')

        img_id = cam_imgs[0]['_id']
        img_date = cam_imgs[0]['taken']
        url = f'http://api.deckchair.com/v1/viewer/image/{img_id}'
        return requests.get(url).content, convert_to_datetime(img_date)

    def fetch_todays(self):
        today = datetime.date.today().strftime('%s')

        cam_imgs = request_to_json(f'http://api.deckchair.com/v1/camera/{self.cam_id}/images?from={today}')

        for img in cam_imgs:
            # print(img['taken'])

            url = f'http://api.deckchair.com/v1/viewer/image/{img["_id"]}'
            yield convert_to_datetime(img['taken']), requests.get(url).content

    def fetch_monthly(self):
        month_ago = (datetime.datetime.now() - datetime.timedelta(days=30))
        unixtime_month_ago = month_ago.strftime('%s')
        start = datetime.datetime.now()
        print(f"Last searched date: {month_ago}")

        running = True
        #           Since this API responds with jsons of a maximum size of 1000 images, we need to
        #           make several requests to gather images from entire month; with every request
        #           I check the last image in it and start from that date on the next request, until
        #           I have all images necessary.
        while running:
            # range as in FROM later TO earlier, dates are in UnixTime
            url = (f'http://api.deckchair.com/v1/camera/{self.cam_id}'
                   f'/images?from={unixtime_month_ago}&to={start.strftime("%s")}')
            cam_imgs = request_to_json(url)

            start = convert_to_datetime(cam_imgs[0]['taken'])
            end = convert_to_datetime(cam_imgs[-1]['taken'])

            print(f"{start} - {end}", url, f"({len(cam_imgs)} images found)")

            for img in cam_imgs:
                img_date = convert_to_datetime(img['taken'])
                if img_date <= month_ago:
                    running = False
                    break
                else:
                    img_url = f'http://api.deckchair.com/v1/viewer/image/{img["_id"]}'
                    yield img_date, requests.get(img_url).content

            start = end

