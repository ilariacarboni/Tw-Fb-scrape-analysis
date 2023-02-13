import tweepy
import configparser
import pandas as pd

config = configparser.RawConfigParser()
config.read('config.ini')

#authentication
bearer_token = config['twitter']['bearer_token']

client = tweepy.Client(bearer_token = bearer_token)

#search query/retrieve data 
query = 'phishing lang:it has:links -is:retweet'
user_fields= ['created_at', 'description', 'entities', 'id', 'location', 'name', 'pinned_tweet_id', 
'profile_image_url', 'protected','public_metrics', 'url', 'username', 'verified', 'withheld']
expansions = ['attachments.poll_ids', 'attachments.media_keys', 'author_id', 'edit_history_tweet_ids', 'entities.mentions.username',
 'geo.place_id', 'in_reply_to_user_id', 'referenced_tweets.id', 'referenced_tweets.id.author_id']
tweet_fields=['context_annotations','author_id', 'created_at']

tweets = client.search_recent_tweets(query=query, tweet_fields=tweet_fields, user_fields=user_fields, expansions=expansions, max_results=10 )

columns = ['UserId','Date', 'Content']
data = []
for tweet in tweets.data:
        author = None
        for user in tweets.includes['users']:
                if user.id == tweet.author_id:
                        author = user
                        break
        if author:
                print(author.username, author.created_at)
        data.append([tweet.author_id, tweet.created_at, tweet.text])

df = pd.DataFrame(data, columns=columns)

df.to_csv('tweets.csv') 
