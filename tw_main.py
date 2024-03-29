import openai_request as openai
from tw_stream import MyStream, db 
import streamlit as st
import plotly.graph_objs as go
import json
import os 
import pandas as pd
import configparser
import graphs

#costants 
FIRST_PROMPT= "\n which of these account might be malcious or spam? give me a list of usernames as an answer"
SECOND_PROMPT="\n these are possible spam accounts,give me some data insights"
#authentication
config = configparser.RawConfigParser()
config.read('config.ini')
bearer_token = config['twitter']['bearer_token']
#get stream of tweets
stream = MyStream(bearer_token)
tweets_data = stream.get_filtered_stream()
#chat gpt function to report accounts
openai_response = openai.get_openai_response(tweets_data+FIRST_PROMPT, 300 )
print(openai_response)

#split the response and store each name as a string in a list
usernames = [name.strip().replace('\n', '') for name in openai_response.split(',')]
users_data = db.get_users(usernames)
#chat gpt function to get users data info
openai_response = openai.get_openai_response(users_data+SECOND_PROMPT,1500) 
print(openai_response)

#create csv file with new and past spam accounts
users_list = json.loads(users_data)
df = pd.DataFrame(users_list)
if os.path.exists('users_data.csv'):
    df.to_csv('users_data.csv', mode='a', header=False, index=False)
else:
    df.to_csv('users_data.csv', index=False)

tweets = db.get_tweets_by_author(usernames)
tweets_json = json.dumps(tweets)
df = pd.read_json(tweets_json)
if os.path.exists('tweets_data.csv'):
    df.to_csv('tweets_data.csv', mode='a', header=False, index=False)
else:
    df.to_csv('tweets_data.csv', index=False)

#create graphs
st.write('Data visualization:')
userdf = pd.read_csv('users_data.csv')
fig = graphs.create_barchart(userdf)
st.plotly_chart(fig)
fig = graphs.create_scatterplot(userdf)
st.plotly_chart(fig)
fig = graphs.create_histogram(userdf)
st.plotly_chart(fig)

st.write('Word count chart:')
tweetdf= pd.read_csv('tweets_data.csv')
fig = graphs.create_wordcount(tweetdf)
st.plotly_chart(fig)
