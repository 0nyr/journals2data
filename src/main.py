__title__ = "journals2data"
__author__ = "onyr, Elöd Egyed-Zsigmond"

import os
import csv
from typing import Any, List

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

# get config data
config_file_path: str = "conf/config.csv"

def load_config(path: str) -> List[data.SourceInfo]:
    with open(path, encoding = 'utf-8', mode = 'r') as file:
        lines: List[str] = file.readlines()
        
        # build list of data.SourceInfo objects
        sources: List[data.SourceInfo] = []
        for line in lines:
            line_data: List[str] = list(line.split(";"))
            try:
                utils.print_list(line_data)
                new_source: data.SourceInfo = data.SourceInfo(
                    line_data[0],
                    line_data[1],
                    line_data[2],
                    line_data[3]
                )
                sources.append(new_source)
            except:
                print("""Error: Fail creating a data.SourceInfo object, 
                possible error with the conf/conf.csv file.""")

    return sources

sources: List[data.SourceInfo] = load_config(config_file_path)
utils.print_list(sources)

def get_config_data(config_file_path) -> dict:
    # get config data from CSV file
    config_data: dict = utils.json_file_to_data(config_file_path)

    # if missing, get list of URLs from csv file
    if config_data.get('journals') == None or config_data['journals'] == "":
        journals: list = []
        # read csv file containing journals
        with open(journals_file_path, encoding='utf-8') as csvf:
            csvReader = csv.DictReader(csvf)
            for row in csvReader:
                journals.append(row['URL'])
        config_data['journals'] = journals
    
    return config_data

#config_data: dict = get_config_data(config_file_path, journals_file_path)

#utils.print_pretty_json(config_data)




# for each journal, get all URLs on the front page
# then decide which ones are URLs of articles
# then for all these URLs, scrap them !


