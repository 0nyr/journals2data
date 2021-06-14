# test file

# test Article Full text extractor
import scraper

testvar = scraper.HelloWorld()
testvar.say_hello()

# url = "http://www.industrie-mag.com/article13165.html"
url: str = "https://www.wsj.com/articles/novavax-covid-19-vaccine-is-90-effective-in-key-study-11623664800?mod=hp_lead_pos3"
try:
    article_scraper: ArticleScraperWithDownload = scraper.ArticleScraperWithDownload(url)
    article_scraper.preprocessAndExtraction()
    print("URL : " + article_scraper.url)
    print("\n")
    print("=======")
    print("Title:" + article_scraper.article.title)

    print("Texte")
    if article_scraper.article_text=="":
        print("texte VIDE")
    print(article_scraper.article_text)
    print("\n")
    print("=======")
    print("\n")
except Exception as e:
    print(e)

