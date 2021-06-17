import typing
import json
import console


class Article():

    url: str = None
    url_source: str = None
    language: str = None
    timestamp_start: str = None
    timestamp_end: str = None
    title_from_link: str = None
    title: str = None
    full_text: str = None

    # WARN: default arguments must be at the end
    def __init__(
        self,
        url: str,
        url_source: str,
        language: str,
        title: str,
        full_text: str,
        timestamp_start: typing.Optional[str]=None,
        timestamp_end: typing.Optional[str]=None,
        title_from_link: typing.Optional[str]=None,
    ):
        self,
        self.url = url
        self.url_source = url_source
        self.language = language
        self.title = title
        self.full_text = full_text
        self.timestamp_start = timestamp_start
        self.timestamp_end = timestamp_end
        self.title_from_link = title_from_link
    
    def __str__(self) -> str:
        return self.to_str(
            pretty = False,
            colors = False
        )
    
    def to_dict(self) -> dict:
        json_str: str = str(self)
        return json.loads(json_str)
    
    def to_str(
        self, 
        pretty: bool = True, 
        nb_spaces: int = 4, 
        colors: bool = True
    ) -> str:
        """
        This function is use to produce a string from the object, 
        but contrary to __str__(self), this one can also produce
        pretty strings in a JSON-like serialization style.
        Supports colors in ANSI/VT100 format.
        """
        # pretty print in JSON-like serialization style
        endl: str = ""
        if(pretty):
            endl = "\r\n"

        spaces: str = ""
        if(pretty):
            for i in range(nb_spaces):
                spaces += " "
        
        # color support for terminals
        reset: str = ""
        key_color: str = ""
        value_color: str = ""
        if(colors):
            reset: str = console.ANSICtrlSequence.RESET.value
            key_color: str = "%s%s%sm" % (
                console.ANSIString.ESC.value,
                console.ANSIString.FG_256.value,
                console.ANSIColorCode.KEY_C.value
            )
            value_color: str = "%s%s%sm" % (
                console.ANSIString.ESC.value,
                console.ANSIString.FG_256.value,
                console.ANSIColorCode.VALUE_C.value
            )
        
        def __pretty_color_line(
            text: str, value: str, end_comma: str = ", "
        ) -> str:
            """
            Internal function to display a line of the serialisez 
            object. Needs to be declare inside "to_str" so as not
            to pass dozens of parameters which would cancel
            the pros of using a function here.
            """
            # standardize behaviour around None / empty str
            if(value == "" or value == None):
                value = "None"
            
            line: str = "%s%s\"%s\"%s: %s\"%s\"%s%s%s" % (
                spaces,
                key_color,
                text,
                reset,
                value_color,
                value,
                reset,
                end_comma,
                endl
            )
            return line
        
        to_string: str = ""
        to_string += "{" + endl
        to_string += __pretty_color_line(
            "url", str(self.url)
        )
        to_string += __pretty_color_line(
            "url_source", str(self.url_source)
        )
        to_string += __pretty_color_line(
            "language", str(self.language)
        )
        to_string += __pretty_color_line(
            "timestamp_start", str(self.timestamp_start)
        )
        to_string += __pretty_color_line(
            "timestamp_end", str(self.timestamp_end)
        )
        to_string += __pretty_color_line(
            "title_from_link", str(self.title_from_link)
        )
        to_string += __pretty_color_line(
            "title", str(self.title)
        )
        to_string += __pretty_color_line(
            "full_text", str(self.full_text), ""
        ) # WARN: no end comma for last JSON element
        to_string += "}"

        return to_string
