import tweepy
from tweepy import StreamingClient,StreamRule
import time
import configparser
import pandas as pd
import json
from database import MongoDb

config = configparser.RawConfigParser()
config.read('config.ini')
api_key = config['twitter']['api_key']
api_key_secret = config['twitter']['api_key_secret']
access_token = config['twitter']['access_token']
access_token_secret = config['twitter']['access_token_secret']

tweet_fields=['context_annotations', "author_id","created_at","entities",'public_metrics']

db = MongoDb("mongodb://localhost:27017/", "tweets_db", "tweets_collection", "users_collection")

class MyStream(tweepy.StreamingClient) :
    tweets = []
    counter=0
    # authentication
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret) 
    api = tweepy.API(auth)

    def on_connect (self) :
        print("Connected")

    def on_tweet (self, tweet):
        if tweet.referenced_tweets == None:
            user_id = tweet.author_id
            user = self.api.get_user(user_id=user_id)
            #data saved in mongodb
            db.insert_tweet(tweet)
            db.insert_user(user)
            #data for openai
            data = { 'Username': [user.screen_name],'Followers': user.followers_count, 'following': user.friends_count,
                    'account created': [user.created_at.isoformat()],'Text': [tweet.text]
                    }
            self.tweets.append(data)
            self.counter += 1
            time.sleep(0.2)
            if self.counter >= 12: #limit number of tweets
                self.disconnect()

    def get_filtered_stream(self):
        #add rule
        rule = StreamRule(value="(check OR see OR here OR click OR free) has:links -is:retweet lang:en")
        self.add_rules(rule)
        self.filter(expansions="author_id",tweet_fields=tweet_fields)
        #conversion to json
        tweets_json = json.dumps(self.tweets)
        print(tweets_json)
        return tweets_json
