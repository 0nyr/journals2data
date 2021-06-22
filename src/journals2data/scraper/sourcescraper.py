from typing import List, Any

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from journals2data import data
from journals2data import utils

class SourceScraper:

    source: data.Source
    known_article_urls: List[str]
    raw_urls: Any #: List[str] # TODO: tmp, check real data structure

    def __init__(
        self,
        source: data.Source,
    ):  
        self.source = source

        self.known_article_url = []
    
    def scrap_all_urls(self):
        """
        Get all URLs from sources:
            + 1) retrieve all URLs str from source
        """
        # TODO: scrap all links from source page
        # add previous code for URL recuperation using request
        self.raw_urls = self.__get_all_website_links(self.source.url)

    # web scraping functions
    def __is_valid(self, url: str):
        """
        Checks whether `url` is a valid URL.
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def __get_all_website_links(self, url: str):
        """
        Returns all URLs that is found on `url` in which it belongs to the same website
        """
        internal_urls = {}
        # all URLs of `url`
        urls = set()
        # domain name of the URL without the protocol
        domain_name = urlparse(url).netloc
        soup = BeautifulSoup(requests.get(url).content, "html.parser")
        for a_tag in soup.findAll("a"):
            href = a_tag.attrs.get("href")
            if href == "" or href is None:
                continue
            href = urljoin(url, href)
            parsed_href = urlparse(href)
            if parsed_href.query !='':
                href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path + '?'+ parsed_href.query  
            else:
                href = parsed_href.scheme + "://" + parsed_href.netloc + parsed_href.path

                    
            if not self.__is_valid(href):
            # not a valid URL 
                continue   
                
            if href in internal_urls:
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
            internal_urls[title] = href
            print(title + ";" + href + ";")

        return internal_urls