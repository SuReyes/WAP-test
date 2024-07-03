import time

import pytest

from pages.twitch_home_page import TwitchHomePage


@pytest.mark.usefixtures("driver_setup")
class TestTwitch:

    @pytest.fixture(autouse=True)
    def class_setup(self, driver_setup):
        self.twitch = TwitchHomePage(self.driver)

    def test_twitch(self):
        # Step 1 go to Twitch
        self.twitch.loadPage()
        # Step 2 click in the search icon
        self.twitch.tap_search()
        # Step 3 input StarCraft II
        self.twitch.search("StarCraft II")
        # Step 4 scroll down 2 times
        self.twitch.scroll()
        self.twitch.scroll()
        # Step 5 Select one streamer
        self.twitch.select_streamer()
        # Step 6 on the streamer page wait until all is load and take a screenshot
        self.twitch.validate_video_is_loaded()
        self.twitch.take_screenshot()
