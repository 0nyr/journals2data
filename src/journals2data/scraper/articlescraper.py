import typing
import datetime
import re

from selenium.common.exceptions import WebDriverException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import newspaper
import unicodedata

from journals2data import data
from journals2data import console

class ArticleScraper:

    article: data.Article
    is_browser_headless: bool
    

    def __init__(
        self, 
        article: data.Article,
        is_browser_headless: bool = True
    ):
        self.article = article
        self.is_browser_headless = is_browser_headless

    def scrap(self, raw_html: str = "") -> typing.Optional[data.Article]:
        """
        This function is used to scrap content from the web
        of the Article using selenium.
        Optionally, the function can take direct raw html.
        It retuns itself if the scraping was successful.
        It returns None if the article is no more available online.
        FIXME: what to do when scraping failed or timeout ?
        """
        
        try:
            # open browser
            browser: webdriver.Firefox
            if self.is_browser_headless:
                fireFoxOptions = webdriver.FirefoxOptions()
                fireFoxOptions.set_headless()
                browser = webdriver.Firefox(firefox_options = fireFoxOptions)
            else:
                browser = webdriver.Firefox()

            # get raw html
            if(raw_html == "" or raw_html == "null"):
                self.article.raw_html = self.__get_article_raw_html(
                    browser
                )
            else:
                self.article.raw_html = raw_html

            # extract content using newspaper from raw html
            self.__extract_data_from_raw_html()

        finally:
            try:
                browser.close()
            except:
                pass
    
    def __get_article_raw_html(self, browser: webdriver.Firefox) -> str:
        """
        Scrap raw html using selenium
        FIXME: what to do when scraping failed or timeout ?
        TODO: implement timeout
        """
        raw_html: str = ""
        browser.get(self.article.url)
        raw_html = browser.page_source
        return raw_html

    def __extract_data_from_raw_html(self):
        """
        This method is used to retreive information from the 
        raw html using newspaper3k to self.article.
        WARN: do not confuse data.Article with newspaper.Article!
        """
        newspaper_article: newspaper.Article(self.article.url)
        # simulate download but by passing to it raw html instead
        newspaper_article.download(self.article.raw_html)

        def preprocess_raw_html(html_code: str) -> str:
            """
            Preprocess the html code by removing the "q" tag 
            and all tags about any table.
            """
            html_code = html_code.replace("<q>", '')
            html_code = html_code.replace("</q>", '')
            html_code = html_code.replace("</table>", '')
            html_code = html_code.replace("<tbody>", '')
            html_code = html_code.replace("</tbody>", '')
            html_code = html_code.replace("</tr>", '')
            html_code = html_code.replace("</td>", '')

            regextable = r"<table(.*?)>"
            regextr = r"<tr(.*?)>"
            regextd = r"<td(.*?)>"
            subst = "/n"
            html_code = re.sub(regextable, subst, html_code, 0, re.MULTILINE)
            html_code = re.sub(regextd, subst, html_code, 0, re.MULTILINE)
            html_code = re.sub(regextr, subst, html_code, 0, re.MULTILINE)
            return html_code

        newspaper_article.html = preprocess_raw_html(
            newspaper_article.html
        )

        # newspaper3k parsing
        newspaper_article.parse()

        # full text cleaning
        article_text = newspaper_article.text
        text = unicodedata.normalize(
            'NFKC', article_text).encode('utf-8', 'ignore')
        article_text = text.decode("utf-8")
        self.article.full_text = article_text

        # add last data from newspaper_article to article
        self.article.title_from_page = newspaper_article.title
        self.article.publish_date = newspaper_article.publish_date

        # log first scraping instant as self.timestamp_start
        if(self.timestamp_start == None or self.timestamp_start == ""):
            self.timestamp_start = datetime.datetime.now().strftime("%S_%M_%H_%d_%m_%Y")



