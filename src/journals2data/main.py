__title__ = "journals2data"
__author__ = "onyr"

import os
import csv
from typing import Any, List

import json

# personal imports
import utils
import console
import data


# debugging
DEBUG: bool = True

if DEBUG:
    console.println_debug(
        "Python Current Working directory = " + str(os.getcwd())
    )



# get sources from config data
config_file_path: str = "conf/config.csv"

def load_config(path: str) -> List[data.Source]:
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
                    # TODO: correct declaration
                    line_data[0],
                    line_data[1],
                    line_data[2],
                    line_data[3]
                )
                sources.append(new_source)
            except:
                print(
                    """Error: Fail creating a data.Source object, 
                    possible error with the conf/conf.csv file."""
                )

    return sources

sources: List[data.Source] = load_config(config_file_path)

print("********* sources list content *********")
for source in sources:
    print(source.to_str(pretty = False))

# for each journal, get all URLs on the front page
# then decide which ones are URLs of articles
# then for all these URLs, scrap them !


