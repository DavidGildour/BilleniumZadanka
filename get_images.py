#!/usr/bin/env python3

import os

from image_fetcher import ImageFetcher
from sys import argv


def main(camera: str, mode=None):
    fetcher = ImageFetcher(camera)

    if fetcher.cam_found:
        print(f"Successfully loaded {fetcher.cam_name} camera.")
    else:
        print("Failed to load desired camera, check url.")
        return

    if mode in ('--latest', None):
        img, img_date = fetcher.fetch_latest()
        file = f'{fetcher.cam_name}_{img_date}.jpg'.replace(" ", "_")
        with open(file, 'wb') as f:
            f.write(img)

        print(f"Image successfully saved as {file}.")

    elif mode == '--todays':
        path = './todays_imgs/'
        if not os.path.exists(path):
            os.mkdir(path)
        count = 0
        for img_date, img in fetcher.fetch_todays():
            with open(f"{path}{img_date.hour}:{img_date.minute}.jpg", 'wb') as f:
                f.write(img)
                print(f"Saved image no. {count}.")
            count += 1
        print(f'Images successfully saved to directory {path}.')

    elif mode == '--monthly':
        count = 0
        path = './last_month/'
        if not os.path.exists(path):
            os.mkdir(path)
        for img_date, img in fetcher.fetch_monthly():
            sub_path = f"{path}{img_date.month}-{img_date.day}/"
            if not os.path.exists(sub_path):
                os.mkdir(sub_path)
            file = f"{sub_path}{img_date.hour}:{img_date.minute}.jpg"
            with open(file, 'wb') as f:
                f.write(img)
            count += 1
        print(f"Successfully saved {count} images.")


if __name__ == '__main__':
    if len(argv) < 2:
        print("Usage:   ./get_images.py URL                                                     [--flags]\n"
              "Flags available:                                                                  --latest\n"
              "                                                                                  --todays\n"
              "                                                                                  --monthly\n"
              "Example: ./get_images.py https://camera.deckchair.com/st-regis-le-morne-mauritius --latest")
    elif len(argv) == 2:
        target_cam = argv[1].split('-')[-1].capitalize()
        main(target_cam)
    else:
        target_cam = argv[1].split('-')[-1].capitalize()
        main(target_cam, argv[2])
