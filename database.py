import pymongo
import pandas as pd
from datetime import datetime

class MongoDb:
    def __init__(self, url, database, tweets_collection, users_collection):
        self.client = pymongo.MongoClient(url)
        self.db = self.client[database]
        self.tweets_collection = self.db[tweets_collection]
        self.users_collection = self.db[users_collection]
    
    def insert_tweet(self, tweet):
        tweet_document = {
            'text': tweet.text,
            'author_id': tweet.author_id,
            'interactions':tweet.public_metrics,
            'source': tweet.source if tweet.source else None,
            'context_annotations': tweet.context_annotations
        }
        self.tweets_collection.insert_one(tweet_document)

    def insert_user(self, user):
        user_document = {
            'author_id': user.id,
            'username': user.screen_name,
            'CreatedAt': user.created_at,
            'Url':user.url,
            'FollowersCount': user.followers_count,
            'FollowingCount': user.friends_count,
            'StatusesCount': user.statuses_count
        }
        self.users_collection.insert_one(user_document)

    def get_tweets_by_author(self, userslist):
        #documents in the collection that have a 'username' that matches any of those in the list
        user_documents = self.users_collection.find({'username': {'$in': userslist}})

        #list of author_ids for the found user documents
        author_ids = [doc['author_id'] for doc in user_documents]
        
        tweet_documents = self.tweets_collection.find({'author_id': {'$in': author_ids}})
        tweets = []
        for doc in tweet_documents:
            #convert MongoDB ObjectId to a string
            doc['_id'] = str(doc['_id'])
            tweets.append(doc)
            
        return tweets
    
    def get_users(self, userslist):
        user_documents = self.users_collection.find({'username': {'$in': userslist}})

        #convert to DataFrame
        users_df = pd.DataFrame(list(user_documents))
        users_df = users_df.drop('_id', axis=1)
    
        #convert to a JSON string using the 'records' orientation
        users = users_df.to_json(orient='records') #, date_format='iso'
        '''
        #update spam user documents as reported
        self.users_collection.update_many(
            {'username': {'$in': userslist}},
            {'$set': {'reported': 'yes'}}
        )
        '''
        return users