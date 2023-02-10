import tweepy
from tweepy import StreamingClient, StreamRule
import time
import configparser
import requests
import pandas as pd

config = configparser.RawConfigParser()
config.read('config.ini')

#authentication
bearer_token = config['twitter']['bearer_token']

tweet_fields=['context_annotations', "referenced_tweets","lang","author_id","created_at","entities"]

class MyStream(tweepy.StreamingClient) :
    def on_connect (self) :
        print("Connected")

    def on_tweet (self, tweet):
        if tweet.referenced_tweets == None:
            #print(f"{tweet.author_id} {tweet.created_at} : {tweet.text}")
            user_id = tweet.author_id
            date = tweet.created_at
            content = tweet.text

            data = {'UserId': [user_id], 'Date': [date],'Text': [content]}
            df = pd.DataFrame(data)

            with open('tweets-stream.csv','a', encoding="utf-8") as f:
                df.to_csv(f, header=False)

            time.sleep(0.2)

stream = MyStream(bearer_token)

#remove pre-existing rules
rule_ids = []
result = stream.get_rules()
for rule in result.data:
    print(f"rule marked to delete: {rule.id} - {rule.value}")
    rule_ids.append(rule.id)
 
if(len(rule_ids) > 0):
    stream.delete_rules(rule_ids)
    printer = MyStream(bearer_token)
else:
    print("no rules to delete")

#add rule
rule = StreamRule(value="get has:links lang:en")
stream.add_rules(rule)
stream.filter(expansions="author_id",tweet_fields=tweet_fields)

