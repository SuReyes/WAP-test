import logging
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

@pytest.fixture(scope="function", params=["chrome"])
def driver_setup(request, browser="chrome"):
    logger.info("Running one time setUp")
    driver = get_driver(browser)
    if request.cls is not None:
        request.cls.driver = driver
    yield driver
    driver.quit()
    logger.info("Running one time tearDown")


def get_driver(browser: str = 'chrome'):
    driver = None

    if browser == "chrome":
        logger.info("Running tests on mobile Chrome")
        mobile_emulation = {"deviceName": "Nexus 7"}

        s = Service(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
        driver = webdriver.Chrome(service=s, options=chrome_options)

        return driver
