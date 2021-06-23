# Journals2Data

### Useful links

##### Internship

[Google drive](https://drive.google.com/drive/folders/1TMXp8a-w8gT9m85oas4vVlC_5WxnGZXQ)

[Google doc report](https://docs.google.com/document/d/1Puyytyf1mq6PpvFar1PQ_91NqK7eE1bbRsUNZP1BROA/edit#)

## Objectif

Development of a deployable Python library allowing the use of online  scraping functions at regular intervals, through the use of pre-trained models.

##### Input: CSV (or JSON?) config file

* URLs of journals to scrap
* Scraping frequency, interval durations
* Path for out files
* Language of journals, used to select the correct pre-trained model.

##### Output: JSON file containing articles

* URL of the journal
* URL of the article
* Timestamp of scaping
* (if available) date of publication of the article
* Title
* Full text

### Input

inside `conf/`, a .csv file with a list of source URLs, language and scraping frequency associated with each URL.

### Output

A big JSON file containing unique scraped articles with metadata and full text.

## Notes

##### long strings in json file

On JSON files with long string, use `ALT`+`Z` to change between word vrap mode or not. The long string can either be displayed entirely or be troncated only visualy by VSCode and ended with `...`.

## Work logs

### Mon 14th June 2021

I have created the package architecture and implemented a way to get user-defined configurations. It works fine.

I have installed `Newpaper3k`, `unidecode` and tested the basic article full text scraper over a set of preselected URLs of articles. It seems to work fine, however, since I don't have access behind some paywalls, I can't scrap everything. I need more time to analyse the results of the test scraping process.

I have also tried to install WSL on windows but the installation is very slow and not finished yet. The DSI also made my account RDP ready for future remote use should I need to tweak stuff from the lab computer.

* I still do not have a wired connection for my laptop, hence cannot have an IPv6 and RDP on my main computer. Re-ask the DSI to do it.
* Continue to develop the Article scraper, and automate tests
* Analyse further the results of the scraping.

### Tue 15th June 2021

Installed WSL1, then WSL2 on the lab pc.

Modified the program input to be only CSV.

* ?: How to ask for the out file path, which should be the same for all articles ? For now, it is hard coded in`main.py` file. -> Ok, 1 path per source

Test write results to a csv

* [ ] Modify the input from CSV (currently working on it).
* [X] Add several languages and articles from my own dataset
* [ ] Test article scraping to a file
* [ ] Test recurrent scrapping
* [ ] Test threads and concurent writing to a file
* [X] Make a URL source set with no paywall from manual verifications.

I have added new classes like `SourceInfo` to build a more robust clean code solution for loading configs. This is still buggy and need a fix.

Added support for Python3 static typing features, with custom types and options.

> NB: some websites have paywalls only over certain articles.

### Wed 16th June 2021

DroPped WSL for VirtualBox. Installed Ubuntu20.04 and fixed some problems with VirtualBox.

* ?: Still can't know why the multi-screen support of VB fails... ?

Continued to work on library foundations, with OOP, serialization, unit testing. Basic unit testing is to be finish tomorrow.

* [X] Fix error at creation of `data.Source` objects
* [X] Added `str` conversion support
* [X] Added `dict` conversion support
* [X] Modify the input from CSV (currently working on it)
* [X] URGENT: Add git to VScode !
* [X] Fix object instantiation
* [X] Add color support for `data.Source` `str` conversion
* [X] Implement Unit Tests (Working on it, see [unittest doc](https://docs.python.org/3/library/unittest.html#unittest.TestLoader.discover) and [StackOverflow](https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure).
* [ ] Complete Article class
* [ ] Add a write to file function, don't use semaphore for now
* [ ] Use hash-map to create a list of ongoing Articles inside he Source object
* [ ] Test article scraping to a file
* [ ] Test recurrent scrapping
* [ ] Test threads and concurent writing to a file with semaphores
* [ ] Perform integration of threads into Source object

### Thu 17 June 2021

Fixed several problems with uniitest. Now the basis is properly working for anyone wanting to implement Unit tests.

Finished the basis data structure for data of the program.

Started working on Newspaper3K scrapper refactoring as well as data extraction from web pages.

* [X] Implement Unit Tests (Working on it, see [unittest doc](https://docs.python.org/3/library/unittest.html#unittest.TestLoader.discover) and [StackOverflow](https://stackoverflow.com/questions/1896918/running-unittest-with-typical-test-directory-structure).
* [X] Complete Article class
* [X] Add a write to file function, don't use semaphore for now
* [X] ~~Use hash-map to create a list of ongoing Articles inside the Source object~~. Used `list` instead because we will need to iterate over its elements to see which articles have disappeared.
* [X] Install Newspaper3k and Unidecode
* [ ] Fix circular import errors due to type hinting. Chech [that fix](https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-fix-circular-imports/) (WIP)
* [ ] Try article scraping to a file (WIP)
* [ ] Try link extraction, create link extraction module
* [ ] Try recurrent scrapping
* [ ] Try threads and concurent writing to a file with semaphores
* [ ] Perform integration of threads into Source object

### Fri 18 June 2021

Updated VSCode with `Pylance` to ensure strong type-checking, but many errors need to be corrected. Some are clearly not simple like the Enum variable attribute strong enforced typing to int. I had to open a [StackOverflow](https://stackoverflow.com/questions/68032592/python-enum-strongly-type-the-value-attribute-to-be-str-or-a-custom-type). Too complex for now. I leave problems there for now.

New Python version do not correctly detect packages. Need to fix that too.

I implemented a script to check the relevance of scraping results given by Newspaper3K. `script_test_n3k.py` uses N3K to scrap a list of articles. I made by hand a list of the expected result. Then it computes the distance in characters between the two strings and compute a score for each scraped article.

> WARN: The `nltk.edit_distance()` function is really slow.

The relevance of the score needs to be relativized since it's quite long even for a human to get a better understanding of the difference between the manual and N3K scraping result.

> NB: Manually scraped raw full_text cannot be put into a JSON since JSON does not support the """ feature for multi-line strings.
>
> And with a CSV, need to clean the output of any ";" symbol.
>
> The best is to stay with python multi-line """ strings.

In the near future, a good idea would be to perform a similar test with BeautifulSoup and Selenium text extraction if such a process is possible. The objective is to detect the difference and understand which solution give the best score, and what actually happen in details.

* [X] ~~Update to Python 3.10~~ to remove type errors like [How do I type hint a method with the type of the enclosing class?](https://stackoverflow.com/questions/33533148/how-do-i-type-hint-a-method-with-the-type-of-the-enclosing-class). Only update to Python3.9.5 since Python3.10 is not currently fully released.
* [X] Evaluate manually newspaper3k scraping against human manual scraping.
* [X] Added several execution files from `__pycache__` to `.gitignore`.
* [ ] Fix Python3.9 broken import. Watch [here](https://www.liquidweb.com/kb/how-to-install-and-update-python-to-3-9-in-ubuntu/) for PATH manipulations and other configs to edit.
* [ ] Fix circular import errors due to type hinting. Chech [that fix](https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-fix-circular-imports/). It did not worked?! (WIP)
* [ ] Fix Enum value attribute type error. Watch [my StackOverflow question](https://stackoverflow.com/questions/68032592/python-enum-strongly-type-the-value-attribute-to-be-str-or-a-custom-type) for an answer. Waiting for an answer. (WIP)
* [ ] Try article scraping to a file (WIP)
* [ ] Install Selenium and get Geckodriver [here for Geckodriver instructions](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/).
* [ ] Test Selenium full-text extraction
* [ ] Score Selenium full-text extraction
* [ ] Install BeautifulSoup
* [ ] Test BeautifulSoup full-text extraction
* [ ] Score BeautifulSoup full-text extraction
* [ ] Try link extraction, create link extraction module
* [ ] Try recurrent scrapping
* [ ] Try threads and concurrent writing to a file with semaphores.
* [ ] Perform integration of threads into Source object

### Mon 21 June 2021

Last week, I tested the HTML extraction and parsing of `newspaper3k`. I'm now going to repeat the same test with `selenium` and `newspaper3` to see how it compares to other libraries.

After some testing, the use of `selenium` degrades a bit the performance of `newspaper3`. Actually, the `newspaper3k` is not built for parsing raw html from another source than `request`! The only way to bypass that is a dirty fix I made, using `article.download` there replacing `article.html` with the raw html from `selenium` but its far from perfect.

* [X] Fix Python3.9 broken import. Watch [here](https://www.liquidweb.com/kb/how-to-install-and-update-python-to-3-9-in-ubuntu/) for PATH manipulations and other configs to edit.
* [X] ~~Fix circular import errors due to type hinting. Chech [that fix](https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-fix-circular-imports/). It did not worked?! (WIP)~~ Feature for upcoming Python3.10
* [ ] Fix Enum value attribute type error. Watch [my StackOverflow question](https://stackoverflow.com/questions/68032592/python-enum-strongly-type-the-value-attribute-to-be-str-or-a-custom-type) for an answer. Waiting for an answer. (WIP)
* [X] Try article scraping to a file (WIP)
* [X] Install Selenium and get Geckodriver [here for Geckodriver instructions](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/).
* [X] Test Selenium raw_html extraction
* [X] Score Selenium full-text extraction
* [X] Install BeautifulSoup
* [ ] Test BeautifulSoup full-text extraction
* [ ] Score BeautifulSoup full-text extraction
* [ ] Try link extraction, create link extraction module
* [ ] Try recurrent scrapping
* [ ] Try threads and concurrent writing to a file with semaphores.
* [ ] Perform integration of threads into Source object

> scikit learn -> arbre de décision

Notes for URL extraction

[scikit RandomForestClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestClassifier.html)

[Stacking Classifiers for higher predictive performance | towards datascience](https://towardsdatascience.com/stacking-classifiers-for-higher-predictive-performance-566f963e4840)

### Tue 22 June 2021

I am conducting further investigations on the results of newspaper3k parsing. I have understood how to pass direct html to it.

Using selenium increases the results of parsing (with corrected test).

* Good 9/11 = 81%
* Bad 2/11 = 18%
* No result with score < 10%

Low score investigations:

[https://www.dailymail.co.uk/news/article-9700729/Double-jabbed-Brits-able-abroad-nearly-170-countries-month.html](https://www.dailymail.co.uk/news/article-9700729/Double-jabbed-Brits-able-abroad-nearly-170-countries-month.html)

From a manual review, it appears that the article was updated, hence the texte has changed and the score between what I had scrapped some days ago and what selenium got is different. This was a false positive.

For [https://finance.yahoo.com/news/stock-market-news-live-updates-june-14-2021-113039717.html](https://finance.yahoo.com/news/stock-market-news-live-updates-june-14-2021-113039717.html) and [https://www.express.co.uk/life-style/health/1451538/coronavirus-uk-update-vaccine-symptom-sneezing](https://www.express.co.uk/life-style/health/1451538/coronavirus-uk-update-vaccine-symptom-sneezing), the problem is that the obtained results are actually RGPD/cooky policy information popups! We need a way to detect/bypass that sort of message.

Example of message:

"Yahoo fait partie de Verizon Media.\n\nEn cliquant sur \u00ab Tout accepter \u00bb, vous consentez \u00e0 ce que Verizon Media et ses partenaires stockent et/ou acc\u00e8dent \u00e0 des informations sur votre appareil par l\u2019interm\u00e9diaire de cookies et technologies similaires, et traitent vos donn\u00e9es personnelles, afin d\u2019afficher des publicit\u00e9s et contenus personnalis\u00e9s, mesurer les performances des publicit\u00e9s et contenus, analyser les audiences et d\u00e9velopper les services.\n\nDonn\u00e9es personnelles pouvant \u00eatre utilis\u00e9es\n\nInformations relatives \u00e0 votre compte, \u00e0 votre appareil et \u00e0 votre connexion internet, y compris votre adresse IP\n\nInformations relatives \u00e0 votre navigation et historique de recherche lors de l\u2019utilisation des sites web et applications de Verizon Media\n\nLocalisation pr\u00e9cise\n\nEn cliquant sur \u00ab Tout refuser \u00bb, vous refusez tous les cookies et technologies similaires dits non-essentiels mais Verizon Media continuera \u00e0 utiliser des cookies et technologies similaires exempt\u00e9s du consentement. Vous pouvez s\u00e9lectionner l\u2019option \u00ab Personnaliser mes choix \u00bb afin de g\u00e9rer vos pr\u00e9f\u00e9rences.\n\nPour en savoir plus sur la fa\u00e7on dont nous utilisons vos informations, veuillez consulter notre Politique relative \u00e0 la vie priv\u00e9e et notre Politique en mati\u00e8re de cookies. Vous pouvez modifier vos choix \u00e0 tout moment en consultant Vos param\u00e8tres de vie priv\u00e9e.",

I have then heavily revamped the library class and file structure so as to go towards a releasable library. I defined several new object and am now working on the URL scraping from source.

I have concerns around async scraping as well as performance and scheduling. For now, I still rely on `request` and not `selenium` but when time will come, I will need to know how to make all these calls asynchronous.

Need to finish the class `SourceScraper` and test the obtained results.

* [X] ~~Score BeautifulSoup full-text extraction~~ Not made for that. It's just a library to transform HTML into a graph usable in Python.
* [X] Revamp library classes and scripts
* [X] Create base for link extraction.
* [ ] Fix errors of `SourceScraper` and test if it's working with integration with other higherchy objects. (WIP)
* [ ] Try link extraction, create link extraction module
* [ ] Try recurrent scrapping
* [ ] Try threads and concurrent writing to a file with semaphores.
* [ ] Perform integration of threads into Source object

### Wed 23 June 2021

Working on URL scraping integration.


* [X] Fix errors of `SourceScraper` and test if it's working with integration with other higherchy objects. (WIP)
* [ ] Add a scraping timeout error and modify URL scraping from source frontpage accordingly.
* [ ] Try link extraction, create link extraction module
* [ ] Try recurrent scrapping
* [ ] Try threads and concurrent writing to a file with semaphores.
* [ ] Perform integration of threads into Source object


end
