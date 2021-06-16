import typing
from typing import Dict

class Article(dict):

    url_source: str = None
    url: str = None
    timestamp_start: str = None
    timestamp_end: str = None
    title_from_link: str = None
    title: str = None
    full_text: str = None

    def __init__(self):
        self = dict()
