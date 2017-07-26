import sys
from selenium import webdriver
import os
import time
from PIL import Image
from io import BytesIO
import subprocess as sp

#현재 화면을 그대로 파일로 저장합니다
def page_screenshot(driver, file):
    driver.save_screenshot(file)
    return True

#현재 화면을 Crop하여 JPG로 저장합니다
def page_image_resize(driver, file, box=(0, 0, 1024, 768), quality=90):
    img = Image.open(BytesIO(driver.get_screenshot_as_png()))
    cropped_img = img.crop(box).convert('RGB')
    cropped_img.save(file, "JPEG", quality=quality)

def page_record_video(driver, file, box=(0, 0, 1024, 768)):
    cmd_out = ['ffmpeg',
               '-f', 'image2pipe',
               '-vcodec', 'png',
               '-r', '10',  # FPS
               '-i', '-',   # Indicated input comes from pipe
               '-vcodec', 'mpeg4',
               '-crf', '26',
               '-vf', 'scale=1024:768',
               '-vb', '5M',
               file]
    pipe = sp.Popen(cmd_out, stdin=sp.PIPE)

    for i in range(1, 30):
        img = Image.open(BytesIO(driver.get_screenshot_as_png()))
        cropped_img = img.crop(box)
        cropped_img.save(pipe.stdin, "PNG")

    pipe.stdin.close()
    pipe.wait()

    if pipe.returncode != 0:
        raise sp.CalledProcessError(pipe.returncode, cmd_out)


#Chrome Driver의 경우 가상으로 아래 화면까지 저장
def fullpage_screenshot(driver, file):
        print("Starting full page screenshot workaround ...")

        total_width = driver.execute_script("return document.body.offsetWidth")
        total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = driver.execute_script("return document.body.clientWidth")
        viewport_height = driver.execute_script("return window.innerHeight")
        print("Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height,viewport_width,viewport_height))
        rectangles = []

        i = 0
        while i < total_height:
            ii = 0
            top_height = i + viewport_height

            if top_height > total_height:
                top_height = total_height

            while ii < total_width:
                top_width = ii + viewport_width

                if top_width > total_width:
                    top_width = total_width

                print("Appending rectangle ({0},{1},{2},{3})".format(ii, i, top_width, top_height))
                rectangles.append((ii, i, top_width,top_height))

                ii = ii + viewport_width

            i = i + viewport_height

        stitched_image = Image.new('RGB', (total_width, total_height))
        previous = None
        part = 0

        for rectangle in rectangles:
            if not previous is None:
                driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
                time.sleep(0.2)
                driver.execute_script("document.getElementById('topnav').setAttribute('style', 'position: absolute; top: 0px;');")
                time.sleep(0.2)
                print("Scrolled To ({0},{1})".format(rectangle[0], rectangle[1]))
                time.sleep(0.2)

            file_name = "part_{0}.png".format(part)
            print("Capturing {0} ...".format(file_name))

            driver.get_screenshot_as_file(file_name)
            screenshot = Image.open(file_name)

            if rectangle[1] + viewport_height > total_height:
                offset = (rectangle[0], total_height - viewport_height)
            else:
                offset = (rectangle[0], rectangle[1])

            print("Adding to stitched image with offset ({0}, {1})".format(offset[0],offset[1]))
            stitched_image.paste(screenshot, offset)

            del screenshot
            os.remove(file_name)
            part = part + 1
            previous = rectangle

        stitched_image.save(file)
        print("Finishing full page screenshot workaround...")
        return True