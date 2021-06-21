from selenium import webdriver
from selenium.webdriver.firefox.options import Options

from bs4 import BeautifulSoup

import utils

brower = None

# objective: create a DB of raw html so as to compare the results on 
# that for every tests

urls = [
    {
        "url": "https://www.wsj.com/articles/novavax-covid-19-vaccine-is-90-effective-in-key-study-11623664800?mod=hp_lead_pos3"
    },
    {
        "url": "https://eu.usatoday.com/story/news/world/2021/06/14/vladimir-putin-refuses-guarantee-alexei-navalnys-safety-prison/7682827002/"
    },
    {
        "url": "https://edition.cnn.com/2021/06/14/politics/china-nuclear-reactor-leak-us-monitoring/index.html"
    }
]

try:
    # set Firefox headless
    fireFoxOptions = Options()
    fireFoxOptions.headless = True

    brower = webdriver.Firefox(
        options = fireFoxOptions,
        firefox_options=fireFoxOptions,
        log_path="../logs/geckodriver.log"
    )

    # get pages
    for element in urls:
        url = element["url"]

        brower.get(url)
        raw_html = brower.page_source
        element["html"] = raw_html

    # write to file
    utils.save_json_to_file(urls, "../res/raw_html_articles/articles.json")

finally:
    try:
        brower.close()
    except:
        pass





