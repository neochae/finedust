import sys

sys.path.append("..")
sys.path.append("../..")
from finedust.settings.local_setting import *
from finedust.util.screen import *

class SiteImageCrawler:
    def __init__(self, url, file, size=None, crop=None, delay=1):
        self.url = url
        self.file = file
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

        if self.crop is not None:
            page_image_resize(self.driver, self.file, box=self.crop)
        else:
            page_screenshot(self.driver, self.file)

    def start(self):
        self.get_image()

if __name__ == '__main__':
    url = 'https://earth.nullschool.net/#current/particulates/surface/level/overlay=pm10/patterson=125.04,34.80,2967/loc=126.98,37.56'
    size = (1024, 860)
    crop = (0, 0, 1024, 768)
    delay = 10
    file = 'images/nullschool.jpg'

    crawler = SiteImageCrawler(url, file, size=size, crop=crop, delay=delay)
    crawler.start()