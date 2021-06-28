from typing import List, Any
import typing

from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
import pandas as pd
from transformers import DistilBertTokenizerFast
from transformers import TFDistilBertForSequenceClassification
import tensorflow as tf
import numpy as np
from lxml import html
from backpack import get_bagpack, get_attribute_list
from build_xpath import to_xpath # FIXME: which module ?
from sklearn.cluster import DBSCAN


import requests
import json
import datetime as dt

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
        
        """
        dframe: pd.DataFrame = pd.DataFrame(data = {
            "url": [],
            "title_from_a_tag": [],
            "scraped_nb_times": []
        })
        """

        # TODO: for debug purpose only
        print("dframe = [see below] \r\n", dframe.head(20))


        # get model_path depending on the language
        model_dirpath: str = utils.Global.BASE_BERT_MODEL_BASEPATH + \
            utils.Global.BERT_LANGUAGE_DIRS[self.source.language]
        loaded_model = TFDistilBertForSequenceClassification.from_pretrained(model_dirpath)
        tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

        # parse links
        result_df: pd.DataFrame = self.__find_all_links(
            dframe,
            model_dirpath
        )
        print("result_df = [see below] \r\n", result_df.head(20))



    def __find_all_links(
        self, 
        title_link_df: pd.DataFrame, 
        model: str
    ):
        """
        Returns all the URLs that are found on this website
        """
        date_hour = list()
        now = dt.datetime.now()

        ## For each <a> element, retrieve Text & Link
        dict_df = pd.DataFrame(data = {
            "link": title_link_df["url"],
            "DOM": title_link_df["title_from_a_tag"]
        })
        # FIXME: not sure of the initialisation of title and DOM...


        dict_df = dict_df.drop('content', axis=1)

        title_columns = dict_df.iloc[:, 0]

        # Load text classification model
        loaded_model = TFDistilBertForSequenceClassification.from_pretrained(model)
        tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')

        model_results = []

        # For each test sentence related to a link, apply the classifier and get a score from 0 to 1
        for index, row in dict_df.iterrows():
            test_sentence = row['title']
            predict_input = tokenizer.encode(test_sentence, truncation=True, padding=True, return_tensors="tf")
            tf_output = loaded_model.predict(predict_input)[0]
            tf_prediction = tf.nn.softmax(tf_output, axis=1).numpy()[0]
            model_results.append(tf_prediction[1])

        # Remove all links where N_words < 4
        for index, title in enumerate(title_columns):
            if (len(title.split()) < 4):
                model_results[index] = 0

        dict_df['prediction'] = model_results

        threshold = 0.01
        # selecting rows based on condition
        rslt_df = dict_df[dict_df['prediction'] >= threshold]

        rslt_df = rslt_df.drop(['prediction'], axis=1)
        print(rslt_df)

        # get html tree

        tree = html.fromstring(_html)

        a_dom = []

        for link in rslt_df['link']:
            path = urlparse(link).path

            if path == "":
                continue

            a_dom = a_dom + tree.xpath('//a[contains(@href, "' + path + '")]/..')

        dom_list = []

        for a in a_dom:

            if a is None:
                continue
            if a[0].tag != "a":
                continue

            dom_list.append(a)

        # build backpack (WSJTheme--headline--unZqjb45 	attribute=class 	count=1)
        bagpack = get_bagpack(dom_list)

        print(bagpack)

        # build attribute list (WSJTheme--headline--unZqjb45 	attribute=class 	count>1)
        liste_dom = get_attribute_list(dom_list, bagpack)

        ### CLUSTERING ###

        bag_of_words = []
        list_of_vectors = []

        # create bag of words
        for _, dom_df in liste_dom:
            for i in range(dom_df.count()['tag']):
                ref = dom_df['tag'][i] + "." + str(dom_df['parent'][i]) + "." + dom_df['attribute'][i] + "=" + \
                    dom_df['value'][i]
                bag_of_words.append(ref)

        bag_of_words = set(bag_of_words)

        # create vectors
        for _, dom_df in liste_dom:
            ref = ""
            for i in range(dom_df.count()['tag']):
                ref += dom_df['tag'][i] + "." + str(dom_df['parent'][i]) + "." + dom_df['attribute'][i] + "=" + \
                    dom_df['value'][i] + " "

            vector = []
            for w in bag_of_words:
                vector.append(ref.split().count(w))

            list_of_vectors.append(vector)

        ## PREDICTION ##
        X = np.array(list_of_vectors)
        db = DBSCAN(eps=0.5, min_samples=2, metric='cosine').fit(X)  # use cosine similarity to compute the distance

        db.fit(X)
        y_pred = db.fit_predict(X)

        ## CLUSTERS ##
        nb_cluster = y_pred.max() + 1
        print("Nb clusters: " + str(nb_cluster))

        threshold = 0.75  ## add to args
        list_simplified = []

        for i in range(0, nb_cluster):
            cl_vectors = X[y_pred == i]
            mean = cl_vectors.mean(axis=0)

            cl_simplified = np.array((mean > threshold) == True)
            list_simplified.append(cl_simplified)

        b_w = np.array(list(bag_of_words))

        for i in range(0, nb_cluster):
            print(b_w[list_simplified[i]])

            print("\n")

        # BUILD XPATH EXPRESSION
        xpath_list = to_xpath(nb_cluster, b_w, list_simplified)

        # FIND THE CORRECT LINKS
        _dom = []
        liste_href = []
        liste_dom = []
        ns = {"re": "http://exslt.org/regular-expressions"}

        for xpath in xpath_list:
            try:
                _dom = _dom + tree.xpath(xpath, namespaces=ns)
                print("expression validated: {}".format(xpath))
            except:
                print("Invalid expression: {}".format(xpath))


        for a_dom in _dom:
            href = a_dom.get('href')

            text = a_dom.text_content()

            # Handle limit case :if href starts with //domain_name
            if (href is not None and href[:2]) == '//':
                href = href[2:]
                href = href[href.find('/'):]

            if (href is not None and href[0] == '/'):
                href = input + href

            _urlparse = urlparse(href)

            # Filter by extension
            find = re.search(r"\.(jpg|jpeg|svg|xml)$", _urlparse.path)

            if (find is not None):
                continue  # skip

            # Remove get parameters?
            liste_href.append(href)
            liste_dom.append(html.tostring(a_dom))
            date_hour.append(now.strftime("%d/%m/%Y %H:%M:%S"))

        result = pd.DataFrame({'URL': liste_href, 'DOM': liste_dom})
        result['DOM'] = result['DOM'].apply(lambda x: x.decode('utf-8'))

        true_name = list()
        for link in result['URL']:
            if not dict_df.loc[dict_df['link'] == link, 'title'].empty:
                title = dict_df.loc[dict_df['link'] == link, 'title'].iloc[0]
            else:
                title = ''
            true_name.append(title)

        result['title'] = true_name

        # display links

        result = pd.merge(dict_df[['link', 'title', 'DOM', 'prediction']].rename(columns={'link': 'URL'}), result,
                        on=['URL', 'title'], how='left',
                        indicator='predicted_class')

        result['DOM'] = np.where(result.predicted_class == 'both', result.DOM_y, result.DOM_x)
        result['predicted_class'] = np.where(result.predicted_class == 'both', 1, 0)

        result['annotated_class'] = ''

        # Pre-annotate links as positive links if matching the RSS feed
        if not pd.isnull(rss):
            d = feedparser.parse(rss)
            rss_links = [entry.link for entry in d.entries]
            result['annotated_class'] = result['URL'].apply(lambda x: '1' if x in rss_links else '')

        date_time = now.strftime("%d/%m/%Y %H:%M:%S")
        result['datetime'] = date_time

        columns = ['datetime', 'title', 'URL', 'DOM', 'predicted_class', 'annotated_class']

        return result[columns]
    
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





