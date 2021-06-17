import typing
from typing import Dict

class Article():

    url: str = None
    url_source: str = None
    timestamp_start: str = None
    timestamp_end: str = None
    title_from_link: str = None
    title: str = None
    full_text: str = None

    def __init__(
        self,
        url: str,
        url_source: str,
        timestamp_start: str,
        
    ):
        self = dict()
