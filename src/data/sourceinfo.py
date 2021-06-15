import typing
from typing import Dict

SourceInfo = typing.NewType('SourceInfo', Dict[str, str])


class SourceInfo(dict):

    url: str = None
    language: str = None
    scrap_frequency: int = None
    output_filepath: str = None

    def __init__(self):
        self = dict()
    
    @classmethod
    def __init__(
        self, 
        url: str, 
        language: str, 
        scrap_frequency: str, 
        output_filepath: typing.Optional[str]=None
    ):
        self = dict()
        self.url = url
        self.language = language
        self.scrap_frequency = scrap_frequency
        self.output_filepath = output_filepath

    def add_key(self, key: str):
        """
        Function to add a key to the dictionary
        """
        self[key]
