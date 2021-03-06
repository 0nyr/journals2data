"""
This type stub file was generated by pyright.
"""

"""
This class holds configuration objects, which can be thought of
as settings.py but dynamic and changing for whatever parent object
holds them. For example, pass in a config object to an Article
object, Source object, or even network methods, and it just works.
"""
__title__ = ...
__author__ = ...
__license__ = ...
__copyright__ = ...
log = ...
class Configuration:
    def __init__(self) -> None:
        """
        Modify any of these Article / Source properties
        TODO: Have a separate ArticleConfig and SourceConfig extend this!
        """
        ...
    
    def get_language(self): # -> Literal['en']:
        ...
    
    def del_language(self): # -> NoReturn:
        ...
    
    def set_language(self, language): # -> None:
        """Language setting must be set in this method b/c non-occidental
        (western) languages require a separate stopwords class.
        """
        ...
    
    language = ...
    @staticmethod
    def get_stopwords_class(language): # -> Type[StopWordsKorean] | Type[StopWordsHindi] | Type[StopWordsChinese] | Type[StopWordsArabic] | Type[StopWordsJapanese] | Type[StopWords]:
        ...
    
    @staticmethod
    def get_parser(): # -> Type[Parser]:
        ...
    


class ArticleConfiguration(Configuration):
    ...


class SourceConfiguration(Configuration):
    ...


