import typing
from typing import Dict

Source = typing.NewType('Source', Dict[str, str])


class Source:

    url: str = None
    language: str = None
    scrap_frequency: int = None
    output_filepath: str = None
    
    @classmethod
    def __init__(
        self, 
        url: str, 
        language: str, 
        scrap_frequency: str, 
        output_filepath: typing.Optional[str]=None
    ):
        self.url = url
        self.language = language
        self.scrap_frequency = scrap_frequency
        self.output_filepath = output_filepath
    
    def __str__(self):
        return self.to_str(pretty = False, nb_spaces = 0)

    def to_str(self, pretty: bool = True, nb_spaces: int = 4):
        endl: str = ""
        if(pretty):
            endl = "\r\n"

        spaces: str = ""
        if(pretty):
            for i in range(nb_spaces):
                spaces += " "

        to_string: str = ""
        to_string += "{" + endl
        to_string += spaces + "\"url\": " + str(self.url) + ", " + endl
        to_string += spaces + "\"language\": " + str(self.language) + ", " + endl
        to_string += spaces + "\"scrap_frequency\": " + str(self.scrap_frequency) + ", " + endl
        to_string += spaces + "\"output_filepath\": " + str(self.output_filepath) + endl
        to_string += "}"

        return to_string

    def add_key(self, key: str):
        """
        Function to add a key to the dictionary
        """
        self[key]
    
