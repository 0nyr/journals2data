# -*- coding: utf-8 -*-
"""
Imagination is more important than knowledge. --Albert Einstein
"""

__title__ = "journals2data"
__author__ = "Onyr (Florian Rascoussier <florian.rascoussier@insa-lyon.fr)"
__license__ = "GLP-3+"
__all__ = ["console", "data", "scraper", "utils", "newspaper"]

from .configuration import DataCollectorConfiguration
from .datacollector import DataCollector