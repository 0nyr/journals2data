# Journals2Data

### Useful links

##### Internship

[Google drive](https://drive.google.com/drive/folders/1TMXp8a-w8gT9m85oas4vVlC_5WxnGZXQ)

[Google doc report](https://docs.google.com/document/d/1Puyytyf1mq6PpvFar1PQ_91NqK7eE1bbRsUNZP1BROA/edit#)

### TODOs

* [ ] Understand how to read a CSV file and convert it to a dict/json object.

## Objectif

Development of a deployable Python library allowing the use of online  scraping functions at regular intervals, through the use of pre-trained models.

### Input: CSV or JSON config file

* URLs of journals to scrap
* Scraping frequency, interval durations
* Path for out files
* Language of journals, used to select the correct pre-trained model.

### Output: JSON file containing articles

* URL of the journal
* URL of the article
* Timestamp of scaping
* (if available) date of publication of the article
* Title
* Full text
