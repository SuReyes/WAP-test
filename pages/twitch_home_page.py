import datetime
import time

import selenium
from selenium.common import NoSuchElementException, ElementNotVisibleException, ElementNotSelectableException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions


class TwitchHomePage:

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self._search_button = "//a[contains(@aria-label, 'Search')]"
        self._search_box = "//input[contains(@data-a-target, 'tw-input')]"
        self._twitch_channel = "tw-link"
        self._twitch_video = "video-player__overlay"
        self.twitch_video_streamer = "//div[@class='InjectLayout-sc-1i43xsx-0 click-handler zzTJm']"

    def loadPage(self):
        self.driver.get('https://m.twitch.tv/')

    def tap_search(self):
        search_link = self.driver.find_element(By.XPATH, self._search_button)
        search_link.click()

    def search(self, query):
        self.driver.implicitly_wait(3)

        search_box = self.driver.find_element(By.XPATH, self._search_box)
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

        self.driver.find_elements(By.CLASS_NAME, self._twitch_channel)

    def scroll(self):
        self.driver.execute_script("window.scroll({top: window.pageYOffset+250, left: 0, behavior: 'smooth',})")

    def select_streamer(self):
        self.driver.implicitly_wait(10)

        channels = self.driver.find_elements(By.CLASS_NAME, self._twitch_channel)
        selected_channel = None

        for channel in channels:
            if channel.is_displayed():
                if "VIEW ALL" in channel.text.upper():
                    continue
                else:
                    selected_channel = channel
                    break

        self.driver.execute_script("arguments[0].click();", selected_channel)

    def validate_video_is_loaded(self, time_to_wait=350):
        # the modal popup is not presented anymore as far as I could test
        timer = None
        waited = 0.0

        ignored_exceptions = [NoSuchElementException,
                              ElementNotVisibleException,
                              ElementNotSelectableException]
        wait = WebDriverWait(self.driver, 2000, ignored_exceptions=ignored_exceptions)

        while not timer and waited < time_to_wait:
            video = wait.until(expected_conditions.presence_of_element_located((By.XPATH, "//video")))
            timer = float(video.get_attribute("currentTime"))
            if not timer:
                waited += 0.01
                time.sleep(0.01)

    def take_screenshot(self):
        self.driver.save_screenshot(f'../screenshots/twitch_screenshot_{datetime.datetime.utcnow()}.png')
