import tweepy
from tweepy import StreamingClient,StreamRule
import time
import configparser
import requests
import pandas as pd
import json

config = configparser.RawConfigParser()
config.read('config.ini')
bearer_token = config['twitter']['bearer_token']
tweet_fields=['context_annotations', "referenced_tweets","lang","author_id","created_at","entities"]
#newfile
class MyStream(tweepy.StreamingClient) :
    tweets = []
    counter=0

    def on_connect (self) :
        print("Connected")

    def on_tweet (self, tweet):
        if tweet.referenced_tweets == None:
            #print(f"{tweet.author_id} {tweet.created_at} : {tweet.text}")
            user_id = tweet.author_id
            #date = tweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
            content = tweet.text

            data = {'UserId': [user_id], 'Text': [content]}
            df = pd.DataFrame(data)
            with open('tweets-stream.csv','a', encoding="utf-8") as f: df.to_csv(f, header=False)
            self.tweets.append(data)
            self.counter += 1
            time.sleep(0.2)
            if self.counter >= 10: # desired number of tweets
                self.disconnect()

    def get_filtered_stream(self):
        #add rule
        rule = StreamRule(value="click has:links lang:en")
        self.add_rules(rule)
        self.filter(expansions="author_id",tweet_fields=tweet_fields)
        
        tweets_json = json.dumps(self.tweets)
        print(tweets_json)
        return tweets_json
