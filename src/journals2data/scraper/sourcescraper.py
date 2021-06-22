from typing import List

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from journals2data import data

class SourceScraper:

    source: data.Source
    known_article_url: List[str]

    def __init__(
        self,
        source: data.Source,
    ):  
        self.source = source
        
        self.known_article_url = []
    
    def scrap_all_urls(self, browser: webdriver.Firefox):
        """
        Get all URLs from sources:
            + 1) retrieve all URLs str from source
        """
        # TODO: scrap all links from source page


    