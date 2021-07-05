# this is the main object to run the library whithout dealing with
# internal objects

import typing
from typing import List
from newspaper import source

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from journals2data import data
from journals2data import utils
from journals2data import scraper
from journals2data import exception
from journals2data import console
from .configuration import J2DConfiguration

class Journals2Data:

    sources: List[data.Source]
    source_scrapers: List[scraper.SourceScraper]
    config: J2DConfiguration

    def __init__(
        self, 
        config: J2DConfiguration
    ):
        if not isinstance(config, J2DConfiguration):
            raise ValueError(
                "Error: config is not a J2DConfiguration."
            )
        self.config = config
        
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
                source, config
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

        # sources scraping loop 
        for source_scraper in self.source_scrapers:
            # use a SourceScraper object to scrap URLs
            source_scraper.scrap_all_urls()
            source_scraper.keep_known_urls()
            source_scraper.url_lifespan_check()
            source_scraper.save_source_articles()
            source_scraper.determine_article_urls()
            source_scraper.scrap_known_url_articles()
            source_scraper.scrap_new_potential_articles()
        
        # run limit and saving
        self.config.params["RUN_NUMBER"] += 1
        if(
            self.config.params["RUN_NUMBER"] >= 
            self.config.params["NB_RUN_LIMIT"]
        ):
            if(
                self.config.params["VERBOSE"] == 
                utils.VerboseLevel.COLOR
            ):
                console.println_ctrl_sequence(
                    "****** RUN number at maximum. Saving everything.",
                    console.ANSICtrlSequence.PASSED
                )

            for source_scraper in self.source_scrapers:
                source_scraper.save_all_now()

