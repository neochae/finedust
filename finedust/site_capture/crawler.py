import sys
import os
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, '..'))

from finedust.settings.local_setting import *
from finedust.util.screen import *

class SiteImageCrawler:
    def __init__(self, url, file, video=None, size=None, crop=None, delay=1):
        self.url = url
        self.file = file
        self.video = video
        self.size = size
        self.crop = crop
        self.delay = delay
        self.driver = webdriver.PhantomJS(PHANTOM_WEBDRIVER)
        self.driver.implicitly_wait(3)

    def get_image(self):
        if self.size is not None:
            self.driver.set_window_position(0, 0)
            self.driver.set_window_size(self.size[0], self.size[1])
        self.driver.get(self.url)
        time.sleep(self.delay)

        if self.video is not None:
            video_temp = IMAGE_DIR + "temp.mp4"
            page_record_video(self.driver, video_temp, box=self.crop)
            shutil.move(video_temp, self.video)


        if self.crop is not None:
            page_image_resize(self.driver, self.file, box=self.crop)
        else:
            page_screenshot(self.driver, self.file)

    def start(self):
        self.get_image()

if __name__ == '__main__':
    #초미세먼지
    url = 'https://m.search.naver.com/search.naver?query=%EC%B4%88%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80'
    size = (1024, 900)
    crop = (70, 240, 689, 764)
    delay = 10
    file = IMAGE_DIR + 'naver_pm25.jpg'

    crawler = SiteImageCrawler(url, file, size=size, crop=crop, delay=delay)
    crawler.start()

    #미세먼지
    url = 'https://m.search.naver.com/search.naver?query=%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80'
    size = (1024, 900)
    crop = (70, 240, 689, 764)
    delay = 10
    file = IMAGE_DIR + 'naver_pm10.jpg'

    crawler = SiteImageCrawler(url, file, size=size, crop=crop, delay=delay)
    crawler.start()

    #aqicn 사진
    url = 'http://aqicn.org/forecast/seoul/kr/'
    size = (1024, 860)
    crop = (0, 0, 1024, 768)
    delay = 10
    file = IMAGE_DIR + 'aqicn.jpg'

    crawler = SiteImageCrawler(url, file, size=size, crop=crop, delay=delay)
    crawler.start()

    #nullschool 사진
    url = 'https://earth.nullschool.net/#current/particulates/surface/level/overlay=pm10/patterson=125.04,34.80,2967/loc=126.98,37.56'
    size = (1024, 860)
    crop = (0, 0, 1024, 768)
    delay = 10
    file = IMAGE_DIR + 'nullschool.jpg'
    video = IMAGE_DIR + 'nullschool.mp4'

    crawler = SiteImageCrawler(url, file, video=video, size=size, crop=crop, delay=delay)
    crawler.start()
