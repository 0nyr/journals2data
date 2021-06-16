# Journals2Data

### Useful links

##### Internship

[Google drive](https://drive.google.com/drive/folders/1TMXp8a-w8gT9m85oas4vVlC_5WxnGZXQ)

[Google doc report](https://docs.google.com/document/d/1Puyytyf1mq6PpvFar1PQ_91NqK7eE1bbRsUNZP1BROA/edit#)

### TODOs

* [X] Understand how to read a CSV file and convert it to a dict/json object.
* [ ] Understand and fix module error: ModuleNotFoundError: No module named 'scraper.scraper'
* [X] Install Newpaper3k
* [ ] Test Newspaper3k with Elöd code.

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

Droped WSL for VirtualBox. Installed Ubuntu20.04 and fixed some problems with VirtualBox.

* ?: Still can't know why the multi-screen support of VB fails... ?


* [X] Fix error at creation of `data.Source` objects
* [X] Added `str` conversion support
* [X] Modify the input from CSV (currently working on it)
* [ ] Add color support for `data.Source` `str` conversion
* [ ] Implement Unit Tests
* [ ] Complete Article class
* [ ] Add a write to file function, don't use semaphore for now
* [ ] Use hash-map to create a list of ongoing Articles inside he Source object
* [ ] Test article scraping to a file
* [ ] Test recurrent scrapping
* [ ] Test threads and concurent writing to a file with semaphores
* [ ] Perform integration of threads into Source object









end
