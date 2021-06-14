__title__ = "journals2data"
__author__ = "onyr, Elöd Egyed-Zsigmond"

import os
import csv

# personal imports
import utils
import console



# debugging
DEBUG: bool = True

if DEBUG:
    console.println_debug(
        "Python Current Working directory = " + str(os.getcwd())
    )

# get config data
config_file_path: str = "conf/config.json"
journals_file_path: str = "conf/journals.csv"

def get_config_data(config_file_path, journals_file_path) -> dict:
    # get config data from JSON file
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

config_data: dict = get_config_data(config_file_path, journals_file_path)

utils.print_pretty_json(config_data)




# for each journal, get all URLs on the front page
# then decide which ones are URLs of articles
# then for all these URLs, scrap them !


