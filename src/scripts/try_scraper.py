# test file

# run at ".." level
from context import get_python_run_context
get_python_run_context()

from journals2data import scraper



# test Article Full text extractor
test_urls: list = [
    "https://www.wsj.com/articles/novavax-covid-19-vaccine-is-90-effective-in-key-study-11623664800?mod=hp_lead_pos3",
    "https://eu.usatoday.com/story/news/world/2021/06/14/vladimir-putin-refuses-guarantee-alexei-navalnys-safety-prison/7682827002/",
    "https://seekingalpha.com/news/3706075-jpmorgans-ready-for-more-inflation-jamie-dimon-tells-investors",
    "https://edition.cnn.com/2021/06/14/politics/china-nuclear-reactor-leak-us-monitoring/index.html",
    "https://www.ft.com/content/f454033a-9975-4efd-92eb-9cf63306af7f",
    "https://www.nasdaq.com/articles/bitcoin-climbs-near-%2440000-after-musk-says-tesla-could-use-it-again-2021-06-14",
    "https://finance.yahoo.com/news/stock-market-news-live-updates-june-14-2021-113039717.html",
    "https://www.morningstar.com/articles/1042863/morningstar-awards-for-investing-excellence-outstanding-portfolio-manager-nominees"
]

#url = "http://www.industrie-mag.com/article13165.html"
for url in test_urls:
    try:
        article_scraper: scraper.ArticleScraperWithDownload = scraper.ArticleScraperWithDownload(url)
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

        print("**********************************************")

