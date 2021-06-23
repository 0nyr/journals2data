import typing
from typing import Dict, List
import json
import os
import datetime

from .source import Source
from journals2data import scraper
from journals2data import console
import journals2data as j2d


class Article():

    source: Source
    raw_html: str

    # to be save
    url: str
    url_source: str
    language: str
    timestamp_start: typing.Optional[str]
    timestamp_end: typing.Optional[str]
    title_from_source: typing.Optional[str]
    title_from_page: typing.Optional[str]
    full_text: typing.Optional[str]
    publish_date: typing.Optional[str]

    # WARN: default arguments must be at the end
    def __init__(
        self,
        source: Source,
        url: str,
        title: typing.Optional[str]=None,
        full_text: typing.Optional[str]=None,
        timestamp_start: typing.Optional[str]=None,
        timestamp_end: typing.Optional[str]=None,
        title_from_source: typing.Optional[str]=None,
    ):
        self.source = source
        self.url = url
        self.title = title
        self.full_text = full_text
        self.timestamp_start = timestamp_start
        self.timestamp_end = timestamp_end
        self.title_from_source = title_from_source

        # from Source object
        self.language = source.language
        self.url_source = source.url

        self.publish_date = None
        self.title_from_page = None
    
    def __str__(self) -> str:
        return self.to_str(
            pretty = False,
            colors = False
        )
    
    def to_dict(self) -> Dict[str, str]:
        json_str: str = str(self)
        return json.loads(json_str)
    
    def to_str(
        self, 
        pretty: bool = True, 
        nb_spaces: int = 4, 
        colors: bool = True
    ) -> str:
        """
        This function is use to produce a string from the object, 
        but contrary to __str__(self), this one can also produce
        pretty strings in a JSON-like serialization style.
        Supports colors in ANSI/VT100 format.
        """
        # pretty print in JSON-like serialization style
        endl: str = ""
        if(pretty):
            endl = "\r\n"

        spaces: str = ""
        if(pretty):
            for _ in range(nb_spaces):
                spaces += " "
        print
        reset: str = ""
        key_color: str = ""
        value_color: str = ""
        if(colors):
            reset: str = console.ANSICtrlSequence.RESET.value
            key_color: str = "%s%s%sm" % (
                console.ANSIString.ESC.value,
                console.ANSIString.FG_256.value,
                console.ANSIColorCode.KEY_C.value
            )
            value_color: str = "%s%s%sm" % (
                console.ANSIString.ESC.value,
                console.ANSIString.FG_256.value,
                console.ANSIColorCode.VALUE_C.value
            )
        
        def __pretty_color_line(
            text: str, value: str, end_comma: str = ", "
        ) -> str:
            """
            Internal function to display a line of the serialisez 
            object. Needs to be declare inside "to_str" so as not
            to pass dozens of parameters which would cancel
            the pros of using a function here.
            """
            # standardize behaviour around None / empty str
            if(value == "None" or value == "" or value == None):
                value = "null"
            
            line: str = "%s%s\"%s\"%s: %s\"%s\"%s%s%s" % (
                spaces,
                key_color,
                text,
                reset,
                value_color,
                value,
                reset,
                end_comma,
                endl
            )
            return line
        
        to_string: str = ""
        to_string += "{" + endl
        to_string += __pretty_color_line(
            "url", str(self.url)
        )
        to_string += __pretty_color_line(
            "url_source", str(self.url_source)
        )
        to_string += __pretty_color_line(
            "language", str(self.language)
        )
        to_string += __pretty_color_line(
            "timestamp_start", str(self.timestamp_start)
        )
        to_string += __pretty_color_line(
            "timestamp_end", str(self.timestamp_end)
        )
        to_string += __pretty_color_line(
            "title_from_source", str(self.title_from_source)
        )
        to_string += __pretty_color_line(
            "title_from_page", str(self.title_from_page)
        )
        to_string += __pretty_color_line(
            "full_text", str(self.full_text)
        )
        to_string += __pretty_color_line(
            "publish_date", str(self.publish_date), ""
        ) # WARN: no end comma for last JSON element
        to_string += "}"

        return to_string
    
    def save_to_file(self):
        """
        This function is responsible for saving the object as 
        a JSON object.

        TODO: Add verification that the object is not already
        in the file.
        TODO: While implementing threading, make sure no concurrent
        writing can occur.
        """
        filepath: str = self.source.output_filepath
        endl: str = "\r\n"

        # if file does not exist, create one with empty JSON list
        if(os.path.exists(filepath) == False):
            with open(
                filepath, encoding = 'utf-8', mode = 'w'
            ) as file:
                file.write(
                    "[" + endl + "]"
                )

        with open(
            filepath, encoding = 'utf-8', mode = 'r+'
        ) as file:
            lines: List[str] = file.readlines()
            nb_of_lines: int = len(lines)

            # insert line at a line before the last one
            #    + StackOverflow: https://stackoverflow.com/questions/1325905/inserting-line-at-specified-position-of-a-text-file 
            spaces: str = "    "
            lines.insert(nb_of_lines - 1, spaces + str(self) + endl)

            # check if preceding line needs a ',' at its end
            line_before_insertion: str = lines[nb_of_lines - 2]
            if(
                line_before_insertion[:1] != '[' and 
                line_before_insertion[:1] != ']'
            ):
                lines[nb_of_lines - 2] = line_before_insertion.strip('\n') + "," + endl

            file.seek(0)
            file.writelines(lines)
    
    # type: -> typing.Optional[Article]
    def scrap(self, raw_html: str = ""):
        """
        This function is used to scrap content from the web
        of the Article.
        Optionally, the function can take direct raw html.
        It retuns itself if the scraping was successful.
        It returns None if the article is no more available online.
        """
        try:
            article_scraper: scraper.ArticleScraperWithDownload = scraper.ArticleScraperWithDownload(self.url, raw_html)
            article_scraper.preprocessAndExtraction()

            self.title_from_page = article_scraper.article.title
            self.full_text = article_scraper.article_text
            self.publish_date = article_scraper.article.publish_date

            # log first scraping instant as self.timestamp_start
            if(self.timestamp_start == None or self.timestamp_start == ""):
                self.timestamp_start = datetime.datetime.now().strftime("%S_%M_%H_%d_%m_%Y")
            
            return self
        except Exception as e:
            print(e) # TODO: only temporary print

            # define this moment as the final timestamp for scraping
            self.timestamp_end = datetime.datetime.now().strftime("%S_%M_%H_%d_%m_%Y")

            # save the Article
            self.save_to_file()
            return None
