import snscrape.modules.twitter as sntwitter
import pandas as pd

query = "(since:1675646041 until:1675646880 near:Gaziantep)"
tweets = []
limit = 10

for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.date, tweet.user.username, tweet.source, tweet.retweetCount,tweet.viewCount])
      
df = pd.DataFrame(tweets, columns=['Date', 'User','Source', 'Retweets','Views'])
print(df)

#df.to_csv('search-result.csv', sep=',', index=False)
