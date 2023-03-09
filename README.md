# TWandFB-scrape-analysis

## Introduction
This repository represents a tool for scraping data from twitter and facebook using Twitter API and JavaScript APIs on fb.

The data is stored in a Mongodb database or in a AmazonS3 bucket of your own. 

The same data is then retrieved from the storage service and analyzed by ChatGPT or Dall-E.

You can either choose which part of the application to use, Twitter or Facebook, by running one of the two main files: 
```tw_main.py``` or ```fb_group_scrape.py```

The results of the data analysis are then showed as graphs and images on a Streamlit application.

Finally, the application aims to show two different approaches in data scraping, hence it can be easily customized based on your own needs.

## Requirements
Before running the application, add your own API keys and credentials in the ```config.ini``` file.

### How to generate keys

- [Twitter](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api): Create a developer account, generate the keys.
- [Facebook](https://www.facebook.com/login/): Use your credentials email and password.
- [OpenAI](https://platform.openai.com/signup): Create a developer account, generate the key.
- [AamzonsS3](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html): Create an account, generate the keys and create a bucket.

### MongoDB
To run twitter scraping files, you'll need to have MongoDB installed on your machine and running on port 27017.
Follow the MongoDB installation guide to set up MongoDB on your system: [MOngoDB Install](https://www.mongodb.com/docs/manual/installation/) 

Note: The code provided for facebook scraping assumes that you have Chrome installed on your system.
However you can change the driver to use a different browser by importing the corresponding driver and using it to launch the browser.

## Install
 Before running the application, install the required libraries:
 
```bash
 pip install -r requirements.txt
```

## How to run
Depending on what social media you want to scrape you can either run:

```bash
streamlit run tw_main.py

#or

streamlit run fb_group_scrape.py
```


