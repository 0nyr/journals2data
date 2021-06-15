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

# get sources from config data
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
                # TODO: fix error here at creation of objects
                new_source: SourceInfo = data.SourceInfo(
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
print("********* sources *********")
utils.print_list(sources)




# for each journal, get all URLs on the front page
# then decide which ones are URLs of articles
# then for all these URLs, scrap them !


