# this file is necessary to avoid cross imports 
# and "partially initialised module error
from typing import List

from .article import Article

class OngoingArticles:

    articles: List[Article]

    def __init__(self):
        self.articles = []
        # TODO: load articles
    
    #def scrap_articles(self):
        # TODO: finish method
    
    # TODO: circular imports can't be avoided.typing
    # they are only due to typing hints
    #    + fix: https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-fix-circular-imports/ 
