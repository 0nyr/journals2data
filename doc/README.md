# Journals2Data

This library is used to scrap automaticaly online newspapers, by providing a list of newspapers front page URLs.

> Since it is a library, you must call its objects to be able to use it. However, if you directly wants to run it, you can do so by running `python3 cli.cpp --conf_path <path/to/journals2data.conf>`. Just modify the path to be correct.

## Installation

1. Install conda. There is a script you can run at `cmd/install_conda.sh`
2. Install dependencies by creating a virtual environment using conda. Use `conda env create --file environment.yml`.
3. Install geckodriver. There is a script you can run at `cmd/install_gecko.sh`. Before that, make sure you have an available Firefox browser by running `firefox --version`. You should see something like what is shown below. If it is not the case, install firefox.

```shell
(base) onyr@laerys:~$ firefox --version
Mozilla Firefox 89.0.2
```

4. Switch to this virtual environment: `conda activate <venv_name>`.
5. Modify the list of article to scrap by modifying `conf/config.csv`. You can find examples inside `conf/example`.
6. Modify the conf params by making a `conf/journals2data.conf` file. You can find examples inside `conf/example`.

## running

There are 3 ways to use the library.

1. Use the library as any module and import it's top level object to use it. This is the intended way of using the library. See `cli.cpp` to get a basic example on how to use  it.
2. Quick test (working): Run `python3`, then `import journals2data` then try it `

```shell
(py39) onyr@laerys:~/Documents/code/python/journals2data/src$ python3
Python 3.9.5 (default, Jun  4 2021, 12:28:51) 
[GCC 7.5.0] :: Anaconda, Inc. on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import journals2data
Python Current Working directory = /home/onyr/Documents/code/python/journals2data/src
>>> journals2data.main("/home/onyr/Documents/code/python/journals2data/src/journals2data/conf/journals2data.onyr.conf")
****** running J2D [--conf_path: /home/onyr/Documents/code/python/journals2data/src/journals2data/conf/journals2data.onyr.conf]
****** config.params = [see below]
{
    "CONFIG_FILETYPE": "csv",
    "DEFAULT_OUTPUT_FILEPATH": "/home/onyr/Documents/code/python/journals2data/out/out.json",
    "CONFIG_CSV_FILEPATH": "/home/onyr/Documents/code/python/journals2data/src/journals2data/conf/csv/config_3_journals.csv",
    "GECKODRIVER_LOG_FILEPATH": "/home/onyr/Documents/code/python/journals2data/logs/geckodriver.log",
    "BERT_MODEL_BASEPATH": "/home/onyr/Documents/code/models/",
    "BERT_LANGUAGE_DIRS": {
        "en": "BERT_classifier_en/",
        "fr": "BERT_classifier_fr/"
    },
    "DEBUG": true,
    "VERBOSE": 2,
    "DEFAULT_TIMEOUT": 120,
    "SOURCE_TIMEOUT": 120,
    "ARTICLE_TIMEOUT": 120,
    "USER": "onyr",
    "ARTICLE_SCORE_THRESHOLD": null,
    "NB_RUN_LIMIT": 2,
    "RUN_NUMBER": 0,
    "IS_J2D_RUNNING": true,
    "POTENTIAL_ARTICLE_LIMIT": 3,
    "SCHEDULE_SYNC_SCRAP_MIN": 2,
    "J2D_RUN_START_TIME": 1625763583.9314969,
    "ARTICLE_SAVING_OPTION": 1,
    "EMPTY_OUT_FILE": true
}
Default out file [/home/onyr/Documents/code/python/journals2data/out/out.json] content has been erased.
****** SIGINT (CTRL + C) termination handled. ******
^C!!!!!! SIGINT or CTRL-C detected. Trying to exit gracefully !!!!!!
(py39) onyr@laerys:~/Documents/code/python/journals2data/src$ 
```

3. (not working yet, FIX imports ?!) If you wish, you can directly use the library as is by running `python3 cli.cpp --conf_path <path/to/journals2data.conf>`. This file shows a good example on how to manipulate the library.
