__title__ = "journals2data"
__author__ = "onyr, Elöd Egyed-Zsigmond"

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

# TODO: Move that into unit tests
test_source: data.Source = data.Source('a', 'b', "c", None)
print("***************** __str__ ")
print(str(test_source))
print("***************** to_str")
print(test_source.to_str())

print("****** Source to Dict")
source_json: str = str(test_source)
source_dict: dict = json.loads(source_json)
utils.print_pretty_json(source_dict)
# test casting
print("****** Source to Dict casting")
souce_dict_casted: dict = test_source.to_dict()
utils.print_pretty_json(souce_dict_casted)

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


