from finedust.settings.setting import *
from sys import platform as _platform

if _platform == "darwin":
    PHANTOM_WEBDRIVER = PROJECT_DIR + "/phantomjs/mac/bin/phantomjs"
elif _platform == "win32":
    PHANTOM_WEBDRIVER = PROJECT_DIR + "/phantomjs/win/bin/phantomjs.exe"
elif _platform == "win64":
    PHANTOM_WEBDRIVER = PROJECT_DIR + "/phantomjs/win/bin/phantomjs.exe"

# PHANTOM_WEBDRIVER = PROJECT_DIR + "/phantomjs/win/bin/phantomjs.exe"

