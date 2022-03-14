import logging
import time
from collections import OrderedDict
import os
import yaml

import json

from selenium import webdriver

from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located


def _download_cmd(url, output=None):
    cmd = '/home/linuxbrew/.linuxbrew/bin/aria2c --user-agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15" '
    if output is not None:
        cmd += ' --out="{output}" '.format(output=output)

    cmd += " " + url
    print(cmd)
    # cli
    os.system(cmd)
    time.sleep(2)


def _download_youtube(url):
    # todo: how to avoid this
    cmd = "/home/linuxbrew/.linuxbrew/bin/youtube-dl {url}".format(url=url)
    os.system(cmd)
    time.sleep(16)


def format_title(title):
    return title.replace("\n", "_").replace(" ", "_")


def mkdir(path):
    if not os.path.exists(path):
        os.mkdir(path)


class EdxCourse(object):
    def __init__(self,
                 username,
                 pwd,
                 course_url,
                 driver="./bin/chromedriver",
                 work_dir=""):

        options = webdriver.ChromeOptions()

        # options.add_argument('--headless')
        options.add_argument('--start-maximized')

        prefs = {
            "download.default_directory": work_dir,
             "directory_upgrade": True
        }

        options.add_experimental_option("prefs", prefs)

        self.driver = webdriver.Chrome(
            service=Service(driver),
            options=options
        )

        # executable_path=driver,
        # chrome_options=options)

        self.wait = WebDriverWait(self.driver, timeout=60)

        self._login(username, pwd)
        self._goto(course_url)

        course_title = "course-title"

        self.wait.until(
            # until elem is presented
            presence_of_element_located(
                (By.CLASS_NAME, course_title)
            ))

        time.sleep(5)

        title = self.driver.find_element(By.CLASS_NAME, course_title)

        # course name
        root_dir = format_title(title.text)

        mkdir(root_dir)
        os.chdir(root_dir)

    def __call__(self):
        units = self._parse_course()

        for unit_title, sub_units in units.items():
            unit_title = format_title(unit_title)
            mkdir(unit_title)
            os.chdir(unit_title)

            for i, (sub_title, url) in enumerate(sub_units):
                sub_title = format_title(sub_title)
                sub_title = "%d_%s" % (i, sub_title)
                mkdir(sub_title)
                os.chdir(sub_title)

                assets = self._parse_unit(sub_title, url)
                if assets is None:
                    assets = []
                base_path = ""

                for j, item in enumerate(assets):
                    mkdir(str(j))
                    os.chdir(str(j))

                    if item[0] == "pdf":
                        output_path = os.path.join(base_path, "slides.pdf")
                        _download_cmd(item[1], str(output_path))

                    elif item[0] == "video":
                        # download mp4
                        output_path = os.path.join(base_path, item[2] + ".mp4")
                        _download_cmd(item[1], str(output_path))

                    elif item[0] == "youtube":
                        _download_youtube(item[1])

                    elif item[0] == "png":
                        with open(item[2] + ".png", "wb") as fo:
                            fo.write(item[1])
                    else:
                        print(f"Unexpected: {item[1]}")

                    # todo: if none, we snapshot the page
                    #  e.g. exam

                    os.chdir("..")
                os.chdir("..")
            os.chdir("..")

    def _goto(self, url):
        self.driver.get(url)

    def _login(self, username, pwd):
        self._goto("https://edx.org")
        self._goto("https://courses.edx.org/login")

        self.wait.until(presence_of_element_located((By.NAME, "emailOrUsername")))

        uname_input = self.driver.find_element(By.NAME, "emailOrUsername")
        uname_input.send_keys(username)

        pwd_input = self.driver.find_element(By.NAME, "password")
        pwd_input.send_keys(pwd + Keys.RETURN)

        self.wait.until(presence_of_element_located(
            (By.CLASS_NAME, "view-dashboard")))

        # time.sleep(2)

    def _parse_course(self):
        # id="courseHome-outline"
        module_list = self.wait.until(
            presence_of_element_located(
                (By.CLASS_NAME, "list-unstyled")
            ))

        # unit
        module_titles = module_list.find_elements(By.CLASS_NAME, "collapsible-trigger")

        # Skip buggy clicks
        expand_all_btn = self.wait.until(
            presence_of_element_located((By.CSS_SELECTOR, ".btn-outline-primary.btn.btn-block"))
        )
        # expand_all_btn = self.driver.find_element(By.CSS_SELECTOR, ".btn-outline-primary.btn.btn-block")
        expand_all_btn.click()

        # title: Unit 0: Pre-course
        # for title in module_titles:
        #     if title.get_attribute("aria-expanded") == "false":
        #         try:
        #             title.click()   # unfold all item in course
        #         except Exception as e:
        #             logging.error(e)
        #             pass

        # li > div
        expandable_cards = module_list.find_elements(By.CLASS_NAME, "collapsible-card-lg")

        units = OrderedDict()

        for card in expandable_cards:
            # unit title e.g. Unit 0: Pre-course
            unit_name = card.find_element(By.CLASS_NAME, "align-middle").text

            # we look for <ol class=list-unstyled>, loop li
            ol = card.find_element(By.CLASS_NAME, "list-unstyled")
            lis = ol.find_elements(By.TAG_NAME, "li")

            for li in lis:

                try:
                    a = li.find_element(By.TAG_NAME, "a")
                    title = a.text                 # must have some title
                    url = a.get_attribute("href")

                    if unit_name in units:
                        units[unit_name].append(
                            (title, url)
                        )
                    else:
                        units[unit_name] = [
                            (title, url)
                        ]
                except Exception as e:
                    pass

        return units

    def _parse_unit(self, title, url):
        assets = []
        if "discussion" in title:
            return assets

        self._goto(url)
        _ = self.wait.until(
            presence_of_element_located((By.ID, "unit-iframe")))

        # parse each tab
        tabs = self.driver.find_element(By.CLASS_NAME, "sequence-navigation-tabs")

        buttons = tabs.find_elements(By.TAG_NAME, "button")
        for button in buttons:
            button.click()

            _ = self.wait.until(
                presence_of_element_located(
                    (By.CLASS_NAME, "unit-container")
                ))

            time.sleep(5)

            tab_type = button.find_element(By.TAG_NAME, "svg").get_attribute("data-icon")

            if tab_type == "video":

                # videos
                _ = self.wait.until(
                    presence_of_element_located((By.ID, "unit-iframe")))

                self.driver.switch_to.frame("unit-iframe")

                try:
                    video = self.driver.find_element(By.CLASS_NAME, "video-download-button")
                    url = video.get_attribute("href")

                    note = self.driver.find_element(By.TAG_NAME,"h3").text
                    assets.append(("video", url, note))

                except Exception as e:
                    logging.info(e)

                    video = self.driver.find_element(By.CLASS_NAME, "video")  # ?
                    meta = json.loads(video.get_attribute("data-metadata"))

                    url = meta["streams"].split(":")[-1]

                    note = self.driver.find_element(By.TAG_NAME, "h3").text

                    assets.append(("youtube", url, note))

                self.driver.switch_to.parent_frame()
            else:
                # text
                _ = self.wait.until(
                    presence_of_element_located((By.ID, "unit-iframe")))

                unit = self.driver.find_element(By.CLASS_NAME, "unit-container")
                png = unit.screenshot_as_png
                note = self.driver.find_element(By.TAG_NAME, "h1").text

                if "Slides for" in note:
                    self.driver.switch_to.frame("unit-iframe")

                    url = self.driver.find_element(
                        By.PARTIAL_LINK_TEXT,
                        "Slides for"
                    ).get_attribute("href")

                    assets.append(("pdf", url))
                else:
                    assets.append(("png", png, note))
        return assets


def run(): 
    # run() used to take click cli args
    with open('settings.yaml', 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        # print(data)
    
        course = EdxCourse(data["user"], data["psw"], data["course"])
        
        # crawal
        course()


if __name__ == "__main__":
    run()
