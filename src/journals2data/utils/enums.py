# class for global variables and parameters
# WARN: apparently, "global.py" is a bad name for a file

from enum import Enum

class VerboseLevel(Enum):
    """
    This enum is used for a better granularity
    on verbosity.
    """

    NONE = 0
    NO_COLOR = 1
    COLOR = 2