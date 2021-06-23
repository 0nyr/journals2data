from .urlinfo import URLInfo

import typing
from typing import Dict

# custom map (dict): {"url_str": URLInfo}
MapURL2URLInfo = typing.NewType('MapURL2URLInfo', Dict[str, URLInfo])
