# this is a configuration object for the DataCollector class

import typing
from typing import List
import time

from journals2data import data
from journals2data import console
from journals2data import utils

class J2DConfiguration:
    
    # default conf params
    params: dict = {
        "CONFIG_FILETYPE": "csv",
        "DEFAULT_OUTPUT_FILEPATH": "/home/onyr/Documents/code/python/journals2data/out/out.json",
        "CONFIG_CSV_FILEPATH": "/home/onyr/Documents/code/python/journals2data/src/journals2data/conf/config.csv",
        "GECKODRIVER_LOG_FILEPATH": "/home/onyr/Documents/code/python/journals2data/logs/geckodriver.log",
        "BERT_MODEL_BASEPATH": "/home/onyr/Documents/code/models/",
        "BERT_LANGUAGE_DIRS": {
            "en": "BERT_classifier_en/",
            "fr": "BERT_classifier_fr/"
        },
        "DEBUG": True,
        "VERBOSE": utils.VerboseLevel.COLOR,
        "DEFAULT_TIMEOUT": 60,
        "SOURCE_TIMEOUT": None,
        "ARTICLE_TIMEOUT": None,
        "USER": None,
        "ARTICLE_SCORE_THRESHOLD": None,  #TODO: choose a good default value
        "NB_RUN_LIMIT": None,
        "RUN_NUMBER": 0,  # should not be edited by hand
        "IS_J2D_RUNNING": True,  # should not be edited by hand
        "POTENTIAL_ARTICLE_LIMIT": None,
        "SCHEDULE_SYNC_SCRAP_MIN": None,
        "J2D_RUN_START_TIME": None # should not be edited by hand
    }

    def __init__(
        self,
        journals2data_conf_filepath: str,
    ):  
        # IMPT: load journals2data conf
        self.__load_journals2data_conf(journals2data_conf_filepath)

        # apply timeout defaults
        if(self.params["SOURCE_TIMEOUT"] == None):
            self.params["SOURCE_TIMEOUT"] = self.params["DEFAULT_TIMEOUT"]
        if(self.params["ARTICLE_TIMEOUT"] == None):
            self.params["ARTICLE_TIMEOUT"] = self.params["DEFAULT_TIMEOUT"]
        
        # save start time
        if(self.params["J2D_RUN_START_TIME"] == None):
            self.params["J2D_RUN_START_TIME"] = time.time()

        # print arguments
        if(self.params["VERBOSE"] == utils.VerboseLevel.NO_COLOR):
            print("****** config.params = [see below]")
            utils.print_pretty_json(self.params)
        elif(self.params["VERBOSE"] == utils.VerboseLevel.COLOR):
            console.println_debug("****** config.params = [see below]")
            utils.print_pretty_json(self.params)

        
    def __load_journals2data_conf(self, path: str):
        """
        This method load journals2data conf and init all
        global variables for the library.
        """
        custom_conf: dict = {}
        # load conf
        with open(path, encoding = 'utf-8', mode = 'r') as file:
            lines: List[str] = file.readlines()

            for line in lines:
                line = line.replace('\n', '')

                # don't execute blank lines
                if(line == "" or line == " "):
                    continue

                # don't execute comments
                if(line[0] == '#'):
                    continue

                exec(line)
        
        # save modified params
        for param in custom_conf:
            if param in self.params:
                self.params[param] = custom_conf[param]

    
    def get_sources(self) -> List[data.Source]:
        sources: List[data.Source] = []

        if(self.params["CONFIG_FILETYPE"] == "csv"):
            sources = self.__load_sources_from_csv(
                self.params["CONFIG_CSV_FILEPATH"]
            )
        
        return sources

    def __load_sources_from_csv(self, path: str) -> List[data.Source]:
        """
        This function is responsible for loading the config file.
        """
        # make sure the path is executed where it should be at "./"
        import sys
        import os
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        sys.path.append(cur_dir)

        # load sources from csv file
        sources: List[data.Source] = []
        with open(path, encoding = 'utf-8', mode = 'r') as file:
            lines: List[str] = file.readlines()

            # if present, remove the headline
            if(lines[0].find('http') == -1): # the headline do not contain a link
                del lines[0]
            
            # build list of data.Source objects
            for line in lines:
                line = line.replace('\n', '')
                line_data: List[str] = list(line.split(";"))
                try:
                    new_source: data.Source = data.Source(
                        url=line_data[0], 
                        language=line_data[1], 
                        scrap_frequency=line_data[2], 
                        output_filepath=line_data[3],
                        params=self.params
                    )
                    sources.append(new_source)
                except:
                    print(
                        """Error: Fail creating a data.Source object, 
                        possible error with the conf/conf.csv file."""
                    )
        
        return sources
