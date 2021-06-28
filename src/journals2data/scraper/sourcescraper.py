from typing import List, Any
import typing

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import pandas as pd

import requests
import json

import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.INFO)

from journals2data import data
from journals2data import utils
from journals2data import console
from journals2data import exception
from .articlescraper import ArticleScraper
from .mapurlarticlescraper import MapURLArticleScraper

class SourceScraper:

    source: data.Source

    last_known_urls: data.MapURLInfo # URLs scraped from last scraping
    known_article_url_for_rescraping: data.MapURLInfo # scrap to check if modified
    potential_article_urls_for_scraping: data.MapURLInfo # URLs to scrap this time
    raw_frontpage_urls: data.MapURLInfo

    article_scrapers: MapURLArticleScraper # current and past article scrapers

    def __init__(
        self,
        source: data.Source,
    ):  
        self.source = source

        # default values    data.MapURLInfo({})
        self.last_known_urls = data.MapURLInfo()
        self.article_urls_for_scraping = data.MapURLInfo()
        self.raw_frontpage_urls = data.MapURLInfo()
    
    def scrap_all_urls(self):
        """
        Get all URLs from sources:
            + 1) retrieve all URLs str from source
        """
        self.raw_frontpage_urls = self.__get_all_website_links(
            self.source.url
        )

        if(utils.Global.VERBOSE == utils.VerboseLevel.COLOR):
            console.println_debug(
                "raw_frontpage_urls type: " + str(
                    type(self.raw_frontpage_urls)
                ) + 
                "source URL: " + self.source.url
            )

    # web scraping functions
    def __is_valid(self, url: str):
        """
        Checks whether `url` is a valid URL.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

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
        @utils.syncTimeout(30)
        def __get_page_content(
            utl_to_scrap: str
        ) -> typing.Optional[bytes]:
            return requests.get(utl_to_scrap).content

        # handle timeout exception
        try:
            page_bytes = __get_page_content(url)
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
            title = a_tag.getText().strip().lstrip()       
            title = title.replace(';','')
            title = title.replace('""','')
            title = title.replace("\n", "")
            title = title.replace("\t", "")
            if title == "" or title is None:
                continue

            # build return object
            new_frontpage_url: data.FrontpageURL = data.FrontpageURL(
                url=href,
                title_from_a_tag=title
            )
            frontpage_urls[href] = new_frontpage_url

            if(utils.Global.VERBOSE == utils.VerboseLevel.NO_COLOR):
                print(str(new_frontpage_url))
            elif(utils.Global.VERBOSE == utils.VerboseLevel.COLOR):
                print(new_frontpage_url.to_str(pretty=False))

        return frontpage_urls
    
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
        # the articles whose URLs are still inside self.last_known_urls
        ...
    
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

        # TODO: for debug purpose only
        print("dframe = [see below] \r\n", dframe.head(20))







        
    
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
        NB: There is an evaluation of the article scraping score. If too bad,
        the newly created ArticleScraper is not added to 
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





