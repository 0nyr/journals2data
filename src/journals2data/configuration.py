# this is a configuration object for the DataCollector class

import typing
from typing import List

from journals2data import data

class DataCollectorConfiguration:

    # URL;language;scrap-frequency;output_filepath

    DEFAULT_CONFIG_CSV_FILEPATH: str = "./conf/config.csv"

    config_file_type: str
    config_filepath: str

    def __init(
        self,
        config_file_type: str = "csv",
        config_filepath: str = ""
    ):
        self.config_file_type = config_file_type
        self.config_filepath = config_filepath

        # set default csv config filepath
        if(self.config_file_type == "csv"):
            if(self.config_filepath == ""):
                self.config_filepath = self.DEFAULT_CONFIG_CSV_FILEPATH
    
    def get_sources(self) -> List[data.Source]:
        sources: List[data.Source] = []

        if(self.config_file_type == "csv"):
            sources = self.__load_sources_from_csv(self.config_filepath)
        
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
                        line_data[0], # url
                        line_data[1], # language
                        line_data[2], # scrap_frequency
                        line_data[3]  # output_filepath
                    )
                    sources.append(new_source)
                except:
                    print(
                        """Error: Fail creating a data.Source object, 
                        possible error with the conf/conf.csv file."""
                    )
        
        return sources
