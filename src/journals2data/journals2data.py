# this is the main object to run the library whithout dealing with
# internal objects

import typing
from typing import List
from newspaper import source

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from journals2data import data
from journals2data import scraper
from journals2data import exception
from journals2data import console
from .configuration import DataCollectorConfiguration

class Journals2Data:

    sources: List[data.Source]
    source_scrapers: List[scraper.SourceScraper]

    def __init__(
        self, 
        config: typing.Optional[DataCollectorConfiguration] = None
    ):
        # set default config
        if(config == None):
            config = DataCollectorConfiguration()
        
        # get sources
        self.sources = config.get_sources()
        if(len(self.sources) <= 0):
            raise exception.NoSourcesError(
                """
                Error: No sources were found.
                Nothing do do. Terminating.
                """
            )
        
        # create source scrapers
        self.source_scrapers = []
        for source in self.sources:
            source_scraper: scraper.SourceScraper = scraper.SourceScraper(
                source
            )
            self.source_scrapers.append(source_scraper)


    def scrap(self):
        """
        For each source in parallel:
            + 1) get all URLs from source
                    + source_scraper.scrap_all_urls()
            + 2) keep already known article URLs, 
                    + source_scraper.keep_known_urls()
            BONUS: check lifespan of already known URLS
            If too long, act accordingly... ?
            remove them from potentially interesting URLs
                    TODO: not implemented
                    + source_scraper.url_lifespan_check()
            + 3) save articles whose URLs disappeared
                    TODO: not implemented
                    + source_scraper.save_source_articles()
            + 4) determine which ones are potential article URLs
                    TODO: to be finished, crucial
                    + source_scraper.determine_article_urls()
            + 5) scrap already known URLs and check if content was modified
                    TODO: to be finished, crucial
                    + source_scraper.scrap_known_url_articles()
            + 6) scrap new potential Articles
            and evaluate scraping of URLs (entropy/confidence score)
                    TODO: to be finished, crucial
                    + source_scraper.scrap_new_potential_articles()

            FIXME: Not async, needed for schedule and improved performance
            FIXME: not scheduled !!!
        """
        # FIXME: make it async
        # open sync browser connection
        # set Firefox headless
        firefox_options = Options()
        firefox_options.headless = True

        brower = webdriver.Firefox(
            options = firefox_options,
            #service_log_path="./logs/geckodriver.log"
            service_log_path="/home/onyr/Documents/code/python/journals2data/logs/geckodriver.log"
        )


        # TODO: finish function and processes
        for source_scraper in self.source_scrapers:
            # use a SourceScraper object to scrap URLs
            source_scraper.scrap_all_urls()
            source_scraper.keep_known_urls()
            source_scraper.url_lifespan_check()
            source_scraper.save_source_articles()
            source_scraper.determine_article_urls()
            source_scraper.scrap_known_url_articles()
            source_scraper.scrap_new_potential_articles()