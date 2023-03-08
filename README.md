# TWandFB-scrape-analysis

## Introduction
Extracting features from URLs to build a data set for machine learning. The purpose is to find a machine learning model to predict phishing URLs, which are targeted to the Brazilian population.

This repo includes the implementation of our paper:


## Requirements

###

Note: The code provided for facebook scraping assumes that you have Chrome installed on your system.
However you can change the driver to use a different browser by importing the corresponding driver and using it to launch the browser.

## Install

```bash
$ sudo apt-get update && sudo apt-get upgrade
$ sudo apt-get install virtualenv python3 python3-dev python-dev gcc libpq-dev libssl-dev libffi-dev build-essentials
$ virtualenv -p /usr/bin/python3 .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

## How to run

Before running the software, add the API Keys to the Google Safe Browsing, Phishtank, and MyWot in the ```config.ini``` file.

Now, run:

```bash
$ python run.py <input-urls> <output-dataset>
```

## Features implemented

## Results

