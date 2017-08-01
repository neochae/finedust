import sys
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, '..'))

from finedust.settings.local_setting import *
from finedust.site_capture.crawler import *

if __name__ == '__main__':
    # nullschool 사진
    url = 'https://earth.nullschool.net/#current/particulates/surface/level/overlay=pm10/patterson=125.04,34.80,2967/loc=126.98,37.56'
    size = (1024, 860)
    crop = (0, 0, 1024, 768)
    delay = 30
    file = IMAGE_DIR + 'nullschool.jpg'
    video = IMAGE_DIR + 'nullschool.mp4'

    crawler = SiteImageCrawler(url, file, video=video, size=size, crop=crop, delay=delay)
    crawler.start()
