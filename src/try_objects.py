import json
import datetime as dt

# personal imports
import utils
import console
import data



# check data.Source conversion to str
test_source: data.Source = data.Source('a', 'b', "c", None)
console.println_debug("****** data.Source.__str__() ")
print(str(test_source))
console.println_debug("******* data.Source.to_str() ")
print(test_source.to_str())

# check data.Source conversion to dict
console.println_debug("****** Source to Dict")
source_json: str = str(test_source)
source_dict: dict = json.loads(source_json)
utils.print_pretty_json(source_dict)
# test casting
console.println_debug("****** Source to Dict casting")
source_dict_casted: dict = test_source.to_dict()
utils.print_pretty_json(source_dict_casted)



# check data.Article conversion to str
console.println_debug("****** data.Article.__str__() ")
test_article: data.Article = data.Article(
    "https://www.test.com/test.html",
    test_source,
    "Test",
    "This is just a simple test.",
    dt.datetime.now().strftime("%S_%M_%H_%d_%m_%Y"),
    None,
    None
)
print(str(test_article))
console.println_debug("******* data.Article.to_str() ")
print(test_article.to_str())

# check data.Article conversion to dict
console.println_debug("****** data.Article to Dict")
article_json: str = str(test_article)
article_dict: dict = json.loads(article_json)
utils.print_pretty_json(article_dict)
# test casting
console.println_debug("****** data.Article to Dict casting")
article_dict_casted: dict = test_article.to_dict()
utils.print_pretty_json(article_dict_casted)



# check Article writing to a file
# TODO: finish testing



# check Article creation from URL
test_source_url: str = "https://finance.yahoo.com/"
test_url: str = "https://eu.usatoday.com/story/news/world/2021/06/14/vladimir-putin-refuses-guarantee-alexei-navalnys-safety-prison/7682827002/"
