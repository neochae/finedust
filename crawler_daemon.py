import os
import sys
import threading
import time
import subprocess
import signal

import traceback
from functools import wraps
from multiprocessing import Process, Queue


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(BASE_DIR, '.'))
from finedust.settings.local_setting import *
from finedust.custom_data.crawler import *
from finedust.global_data.crawler import *
from finedust.open_data.crawler import *




class CrawlerThread(threading.Thread):
    def __init__(self, name, wait):
        threading.Thread.__init__(self)
        self.name = name
        self.max_waiting = wait
        self._stop = threading.Event()

    def run(self):
        max_waiting = self.max_waiting
        command = "python %s/%s" % (BASE_DIR, self.name)

        while not self.stopped():
            start_time = time.time()
            print("%s start crawling\n" % (self.name))
            subprocess.call(command, shell=True)
            delta = max_waiting - (time.time() - start_time)
            if delta > 0:
                print("%s waiting %d seconds\n" % (self.name, delta))
                time.sleep(delta)

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.isSet()


class GracefulKiller:
    kill_now = False

    def __init__(self):
        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

    def exit_gracefully(self, signum, frame):
        self.kill_now = True


if __name__ == '__main__':
    threads = []
    crawlers = {"custom_data/crawler.py":5*60,
                "global_data/crawler.py":30*60,
                "open_data/crawler.py":30*60,
                "site_capture/crawler.py": 1*60*60}
    for crawler in crawlers.keys():
        thread1 = CrawlerThread(crawler, crawlers[crawler])
        thread1.start()
        threads.append(thread1)

    killer = GracefulKiller()
    while True:
        time.sleep(10)
        if killer.kill_now:
            print("Trying to kill ...")
            for t in threads:
                t.stop()
            for t in threads:
                t.join()
            break

    print("Exiting Crawler main")
