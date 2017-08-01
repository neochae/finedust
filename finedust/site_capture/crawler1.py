import sys
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, '..'))

from finedust.settings.local_setting import *
from finedust.site_capture.crawler import *

if __name__ == '__main__':
    # aqicn 사진
    url = 'http://aqicn.org/forecast/seoul/kr/'
    size = (1024, 860)
    crop = (0, 0, 1024, 768)
    delay = 20
    file = IMAGE_DIR + 'aqicn.jpg'

    crawler = SiteImageCrawler(url, file, size=size, crop=crop, delay=delay)
    crawler.start()
