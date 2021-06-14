import os

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
config_data: dict = utils.json_file_to_data("conf/config.json")

utils.print_pretty_json(config_data)

config_data: dict = 