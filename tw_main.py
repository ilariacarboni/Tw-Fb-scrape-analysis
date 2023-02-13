import tw_snscrape
import openai_request
from tw_stream import MyStream
from tweepy import StreamRule
import configparser

#authentication
config = configparser.RawConfigParser()
config.read('config.ini')
bearer_token = config['twitter']['bearer_token']

stream = MyStream(bearer_token)

#remove pre-existing rules
rule_ids = []
result = stream.get_rules()
for rule in result.data:
    print(f"rule marked to delete: {rule.id} - {rule.value}")
    rule_ids.append(rule.id)
 
if(len(rule_ids) > 0):
    stream.delete_rules(rule_ids)
else:
    print("no rules to delete")
'''
query = "(ferragni since:2023-02-07 until:2023-02-08)"
limit = 50
tweets_data = tw_snscrape.get_tweets(query, limit)
'''
tweets_data = stream.get_filtered_stream()

openai_response = openai_request.get_openai_response(tweets_data)
print(openai_response)