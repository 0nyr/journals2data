import typing

import time
import json

from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import console
import data

class ArticleScraper:

    browser = None

    def __init__(self, is_browser_headless: bool = True):
        self.is_browser_headless = is_browser_headless
        if is_browser_headless:
            fireFoxOptions = webdriver.FirefoxOptions()
            fireFoxOptions.set_headless()
            self.browser = webdriver.Firefox(firefox_options = fireFoxOptions)
        else:
            self.browser = webdriver.Firefox()

    def scrap(self, url: str) -> typing.Optional[data.Article]:
        """
        Load the page at provided URL
        """
        # TODO: complete the function
        
        # get page
        self.browser.get(url)
