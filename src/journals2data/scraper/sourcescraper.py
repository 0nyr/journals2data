from typing import List, Any

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import pandas as pd


import requests
import re

import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

import journals2data
from journals2data import data
from journals2data import utils
from journals2data import console
from journals2data import exception
from journals2data.scraper import url_predict
from .articlescraper import ArticleScraper
from .mapurlarticlescraper import MapURLArticleScraper

class SourceScraper:

    source: data.Source
    config: journals2data.J2DConfiguration

    last_known_urls: data.MapURLInfo # URLs scraped from last scraping
    disappeard_urls_for_saving: data.MapURLInfo # URLs for saving
    known_article_url_for_rescraping: data.MapURLInfo # scrap to check if modified
    potential_article_urls_for_scraping: data.MapURLInfo # URLs to scrap this time
    raw_frontpage_urls: data.MapURLInfo

    article_scrapers: MapURLArticleScraper # current and past article scrapers

    def __init__(
        self,
        source: data.Source,
        config: journals2data.J2DConfiguration
    ):  
        self.source = source
        self.config = config

        # default values    data.MapURLInfo({})
        self.last_known_urls = data.MapURLInfo()
        self.raw_frontpage_urls = data.MapURLInfo()
        self.potential_article_urls_for_scraping = data.MapURLInfo()
        self.known_article_url_for_rescraping = data.MapURLInfo()

        self.disappeard_urls_for_saving = data.MapURLInfo()
    
    def scrap_all_urls(self):
        """
        Get all URLs from source:
            + 1) retrieve all URLs str from source
        """
        self.raw_frontpage_urls = self.__get_all_website_links(
            self.source.url
        )

        if(self.config.params["VERBOSE"] == utils.VerboseLevel.COLOR):
            console.println_debug(
                "raw_frontpage_urls type: " + str(
                    type(self.raw_frontpage_urls)
                ) + 
                "source URL: " + self.source.url
            )

    # web scraping functions
    def __get_all_website_links(
            self, url: str
        ) -> data.MapURLInfo:
        """
        Returns all URLs that is found on `url` in which it belongs 
        to the same website.
        """
        frontpage_urls: data.MapURLInfo = data.MapURLInfo()
        urls = set() # all URLs of `url`

        # domain name of the URL without the protocol
        domain_name = urlparse(url).netloc

        # get raw data from source frontpage, with timeout
        @utils.syncTimeout(self.config.params["DEFAULT_TIMEOUT"])
        def __get_page(
            url_to_scrap: str
        ) -> requests.Response:
            return requests.get(url_to_scrap)

        # handle timeout exception
        try:
            response = __get_page(url)
            page_bytes = response.content
            self.source.set_html(response.text) # page HTML as Unicode
        except exception.Timeout as ex:
            logging.warning(
                """
                Source frontpage scraping for raw URL aborted 
                due to timeout. Concerned source URL: 
                """ + 
                self.source.url
            )
            # timeout limit reached, no URL can be retrieve, return empty
            return frontpage_urls
        
        # parse raw data with BeautifulSoup
        soup = BeautifulSoup(page_bytes, "html.parser")

        # extract URLs and title info from related <a> tags
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            if parsed_href.query !='':
                href = parsed_href.scheme + "://" + \
                    parsed_href.netloc + parsed_href.path + \
                    '?'+ parsed_href.query 
            else:
                href = parsed_href.scheme + "://" + \
                    parsed_href.netloc + parsed_href.path

                    
            if not self.__is_valid(href):
                # not a valid URL 
                continue

            if href in frontpage_urls:
                # already in the set
                continue
            
            if domain_name not in href:
                # external link
                continue
            
            urls.add(href)
            
            raw_title: str = a_tag.getText().strip().lstrip()
            title: str = self.__clean_title_from_a_tag(raw_title)
            if title == "" or title is None:
                continue

            # build return object
            new_frontpage_url: data.FrontpageURL = data.FrontpageURL(
                url=href,
                title_from_a_tag=title
            )
            frontpage_urls[href] = new_frontpage_url

            if(self.config.params["VERBOSE"] == utils.VerboseLevel.NO_COLOR):
                print(str(new_frontpage_url))
            elif(self.config.params["VERBOSE"] == utils.VerboseLevel.COLOR):
                print(new_frontpage_url.to_str(pretty=False))

        return frontpage_urls
    
    def __is_valid(self, url: str):
        """
        Checks whether `url` is a valid URL.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)
    
    def __clean_title_from_a_tag(self, title: str) -> str:      
        title = title.replace(';','')
        title = title.replace('""','')
        title = title.replace("\n", "")
        title = title.replace("\t", "")
        return title
    
    def keep_known_urls(self):
        """
        Keep already known article URLs

            + 1) Iterate through keys (URL strings) of raw_frontpage_urls
            + 2) Check if they are present inside last_known_urls_map
            + 3) If present, add current pair to article_urls_for_scraping
        """
        # iterate trhough the dict keys: https://www.geeksforgeeks.org/iterate-over-a-dictionary-in-python/ 
        for url in self.raw_frontpage_urls:
            # check if url key is present in self.last_known_urls
            if url in self.last_known_urls:
                # transfer pair to self.known_article_url_for_rescraping
                self.known_article_url_for_rescraping[
                    url] = self.raw_frontpage_urls.pop(url)
                # and removes pair from self.last_known_urls, 
                # what remains will be saved after inside save_source_articles()
                del self.last_known_urls[url] # FIXME: not sure it will works
        # all recognised url have been deleted from self.last_known_urls
        # what remains is for saving
        self.disappeard_urls_for_saving = self.last_known_urls

    def url_lifespan_check(self):
        """
        check lifespan of already known URLS
        If too long, act accordingly... ?
        remove them from potentially interesting URLs
        """
        # TODO: do something on self.known_article_urls_for_rescraping
        ...
    
    def save_source_articles(self):
        """
        Save articles whose URLs disappeared.
        """
        # TODO: do something with self.last_known_urls so as to save
        # the articles whose URLs are still inside self.disappeard_urls_for_saving
        # do something with self.article_scrapers 
        #    self.article_scrapers...article.save_to_file()
        for url in self.disappeard_urls_for_saving:
            self.article_scrapers[url].article.save_to_file()
    
    def determine_article_urls(self):
        """
        Determine which ones are potential article URLs. 
        This is a crucial and heavy decision layer, using a range of 
        techniques such as BERT models, recurrence or heuristics for 
        decision-making.

        Objective of the function:
        Determine which URLs from self.raw_frontpage_urls are articles
        and pop them inside self.article_urls_for_scraping    
        """
        # TODO: finish method

        # convert raw_frontpage_urls.values: data.FrontpageURL to pd.DataFrame
        dframe: pd.DataFrame = self.raw_frontpage_urls.to_DataFrame()
        
        """
        dframe: pd.DataFrame = pd.DataFrame(data = {
            "url": [],
            "title_from_a_tag": [],
            "scraped_nb_times": []
        })
        """
        print("dframe = [see below] \r\n", dframe.head(20))

        # parse links through BERT, DOM and heuristics layers
        result_df: pd.DataFrame = self.__link_prediction_layers(dframe)
        print(
            "result_df after __link_prediction_layers= [see below] \r\n", 
            result_df.head(20)
        )

        # url for scraping selection decision based on previous results
        # adding relevant URL to the self.potential_article_urls_for_scraping
        def apply_url_selection(dataframe: pd.DataFrame) -> pd.DataFrame:

            def compute_prediction_score(row: pd.Series):
                # TODO: ameliorate ponderations depending on the key
                # FIXME: what does DOM layer for the score
                prediction_keys_with_ponderation: list = [
                    {"key": "BERT", "ponderation": 0.5},
                    {"key": "h0", "ponderation": 0.7},
                    {"key": "h1", "ponderation": 0.7},
                    {"key": "h2", "ponderation": 1},
                    {"key": "h3", "ponderation": 1.3} 
                ]
                detection_sum: float = 0
                for element in prediction_keys_with_ponderation:
                    detection_sum += row[element["key"]]*element["ponderation"]

                return detection_sum

            dataframe["score"] = 0  # add column for results
            dataframe["score"] = dataframe.apply(
                compute_prediction_score, axis=1
            )

            return dataframe
        
        result_df = apply_url_selection(result_df)
        print(
            "result_df after apply_url_selection = [see below]\r\n", 
            result_df.head(20)
        )

        def transfer_selected_url_for_scraping(row: pd.Series):
            # apply score threshold
            # TODO: ameliorate with decision tree
            if(row["score"] > 2.5):
                # transfer this URL for scraping
                url = row["URL"]
                if url in self.raw_frontpage_urls:
                    # transfer pair from raw to url for scraping
                    self.potential_article_urls_for_scraping[
                        url] = self.raw_frontpage_urls.pop(url)

        result_df.apply(transfer_selected_url_for_scraping, axis=1)

    def __link_prediction_layers(
        self, 
        title_link_df: pd.DataFrame
    ) -> pd.DataFrame:
        """
        Apply BERT, DOM and the heuristic
        determination algorithms so as to get a multiple scores of 
        prediction for a link to be an article or not.
        """
        # pandas printing options
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)

        dframe = pd.DataFrame(data = {
            "link": title_link_df["url"],
            "title": title_link_df["title_from_a_tag"],
            "scrap": title_link_df["scraped_nb_times"]
        })
        print("dframe base = [see below] \r\n", dframe.head(10))

        # [BERT] apply BERT prediction layer
        dframe = url_predict.apply_BERT_prediction(dframe)
        print("dframe columns = ", list(dframe))
        print(
            "dframe after apply_BERT_prediction = [see below] \r\n", 
            dframe.head(10)
        )

        # [DOM] apply DOM prediction layer
        dframe = url_predict.apply_DOM_prediction(
            dframe,
            self.source
        )
        print(
            "dframe after apply_DOM_prediction = [see below] \r\n", 
            dframe.head(10)
        )

        # [h0] apply 4 words on title heuristic 
        dframe = url_predict.apply_heuristic_h0(dframe)
        print(
            "dframe after apply_title_word_count_heuristic = [see below]\r\n", 
            dframe.head(20)
        )

        # [h1] apply h1 heuristic
        dframe = url_predict.apply_heuristic_h1(dframe)
        print(
            "dframe after apply_heuristic_h1 = [see below]\r\n", 
            dframe.head(20)
        )

        # [h2] apply h2 heuristic
        dframe = url_predict.apply_heuristic_h2(dframe)
        print(
            "dframe after apply_heuristic_h2 = [see below]\r\n", 
            dframe.head(20)
        )

        # [h3] apply h3 heuristic
        dframe = url_predict.apply_heuristic_h3(dframe)
        print(
            "dframe after apply_heuristic_h3 = [see below]\r\n", 
            dframe.head(20)
        )

        return dframe
        


    def scrap_known_url_articles(self):
        """
        Scrap URLs that have already been scraped in the passed and check
        if they were modified or not!
        """
        for url in self.known_article_url_for_rescraping:
            article_scraper: ArticleScraper = self.article_scrapers[url]
            # TODO: finish function
            # rescrap article and check if content was modified
            ...
    
    def scrap_new_potential_articles(self):
        """
        Scrap URLs that were not already known as articles but that
        have been marked as potential articles.
        Create an ArticleScraper for each of the URLs and launch 
        scraping process.
        NOTE: There is an evaluation of the article scraping score. 
        If too bad, the newly created ArticleScraper is not added to 
        self.article_scrapers.
        """

        for url in self.potential_article_urls_for_scraping:
            article: data.Article = data.Article(
                self.source,
                url
            )
            article_scraper: ArticleScraper = ArticleScraper(
                article
            )
            # call scraping steps
            # check scraping score
            #    if scraping score good enough, 
            #    add article_scraper to self.article_scrapers
            # TODO: complete function








