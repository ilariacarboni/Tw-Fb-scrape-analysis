import plotly.express as px
import plotly.subplots as sp
import pandas as pd
import nltk
from nltk.corpus import stopwords

def create_barchart(df):
    #include the last 15 rows
    last_15 = df.iloc[-15:]
    last_15['FollowRatio'] = last_15['FollowingCount'] / last_15['FollowersCount']
    chart_data = last_15[['username', 'FollowRatio']].set_index('username')

    fig = px.bar(chart_data, x=chart_data.index, y='FollowRatio', labels={'x':'Username', 'y':'Ratio'})
    fig.update_layout(xaxis_tickangle=-90)
    
    return fig

def create_scatterplot(df):
    #scatter chart
    df['CreatedAt'] = pd.to_datetime(df['CreatedAt'], unit='ms')
    date_counts = df['CreatedAt'].value_counts()
    counts = date_counts.values

    fig = px.scatter(df, x=date_counts.index, y=[1]*len(date_counts), size=counts*10, color=counts,
                 color_continuous_scale=px.colors.sequential.Rainbow,  opacity=0.2, hover_data={'count_size': counts})
    fig.update_layout(xaxis_title='Account Creation Date', yaxis_title='')
    fig.update_traces(marker=dict(line=dict(width=1,color='DarkSlateGrey')))
    return fig
  
def create_wordcount(df):
    all_words = []
    for tweet in df['text']:
        words = tweet.split()
        all_words += [word.lower() for word in words] 
    #remove stopwords
    stop_words = set(stopwords.words('english'))
    query_words = ['see', 'check', 'click','here:','&',',', '-', 'u','get','go' ]
    stop_words.update(query_words)
    filtered_words = [word for word in all_words if word not in stop_words]
    #frequency of each word
    freq_dist = nltk.FreqDist(filtered_words)

    n = 20  #words to show
    words, freqs = zip(*freq_dist.most_common(n))
    data = pd.DataFrame({'word': words, 'frequency': freqs})
    fig = px.bar(data, x='word', y='frequency', labels={'word': 'Words', 'frequency': 'Frequency'})

    return fig