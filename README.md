# Journals2Data

### Useful links

##### Internship

[Google drive](https://drive.google.com/drive/folders/1TMXp8a-w8gT9m85oas4vVlC_5WxnGZXQ)

[Google doc report](https://docs.google.com/document/d/1Puyytyf1mq6PpvFar1PQ_91NqK7eE1bbRsUNZP1BROA/edit#)

##### selenium

[selenium doc](https://www.selenium.dev/documentation/en/) 

##### beautifulsoup

[beautifulsoup doc](https://www.crummy.com/software/BeautifulSoup/bs4/doc/#)





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

Last week, I tested the HTML extraction and parsing of `newspaper3k`. I'm now going to repeat the same test with `selenium` and `BeautifulSoup` to see how it compares to other libraries.

* [ ] Fix Python3.9 broken import. Watch [here](https://www.liquidweb.com/kb/how-to-install-and-update-python-to-3-9-in-ubuntu/) for PATH manipulations and other configs to edit.
* [ ] Fix circular import errors due to type hinting. Chech [that fix](https://adamj.eu/tech/2021/05/13/python-type-hints-how-to-fix-circular-imports/). It did not worked?! (WIP)
* [ ] Fix Enum value attribute type error. Watch [my StackOverflow question](https://stackoverflow.com/questions/68032592/python-enum-strongly-type-the-value-attribute-to-be-str-or-a-custom-type) for an answer. Waiting for an answer. (WIP)
* [ ] Try article scraping to a file (WIP)
* [X] Install Selenium and get Geckodriver [here for Geckodriver instructions](https://www.selenium.dev/documentation/en/webdriver/driver_requirements/).
* [ ] Fix DeprecationWarning: use service_log_path instead of log_path
* [ ] Fix DeprecationWarning: use options instead of firefox_optionsTest Selenium full-text extraction
* [ ] Score Selenium full-text extraction
* [ ] Install BeautifulSoup
* [ ] Test BeautifulSoup full-text extraction
* [ ] Score BeautifulSoup full-text extraction
* [ ] Try link extraction, create link extraction module
* [ ] Try recurrent scrapping
* [ ] Try threads and concurrent writing to a file with semaphores.
* [ ] Perform integration of threads into Source object

end
