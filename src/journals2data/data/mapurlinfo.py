from .frontpageurl import FrontpageURL

import typing
from typing import Dict

"""
This type represents a mapping of key:value pairs
between a URL string as key and a FrontpageURL as value.
The idea is to be able to check at no cost that a specific
URL string is present inside or not, and if so, to be able
to retreive its informations contained inside a 
FrontpageURL object at no cost.
"""
MapURLInfo = typing.NewType('MapURLInfo', Dict[str, FrontpageURL])
