# class for global variables and parameters
# WARN: apparently, "global.py" is a bad name for a file

from typing import Dict

from enum import Enum

class VerboseLevel(Enum):

    NONE = 0
    NO_COLOR = 1
    COLOR = 2


class Global:

    # testing and debugging
    DEBUG: bool = True
    VERBOSE: VerboseLevel = VerboseLevel.COLOR
    V_COLOR: bool = True

    # timeout
    DEFAULT_TIMEOUT: int = 60

    # BERT models
    BASE_BERT_MODEL_BASEPATH: str = "/home/onyr/Documents/code/models/"
    BERT_LANGUAGE_DIRS: Dict[str, str] = {}
    BERT_LANGUAGE_DIRS["en"] = "BERT_classifier_en/"
    BERT_LANGUAGE_DIRS["fr"] = "BERT_classifier_fr/"

