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

def create_histogram(df):
    #group data by creation date
    df['CreatedAt'] = pd.to_datetime(df['CreatedAt'], unit='ms')
    grouped_data = df.groupby('CreatedAt')['author_id'].count().reset_index()

    #create plotly fig
    fig = px.histogram(grouped_data, x='CreatedAt', y='author_id', nbins=80, title='Distribution of Account Creation Dates', marginal='rug')

    #axis name
    fig.update_layout(
        xaxis_title='Account Creation Date',
        yaxis_title='Number of Accounts'
    )
    #change color
    fig.update_traces(marker=dict(color='darkturquoise'))

    return fig

def create_scatterplot(df):
    df['CreatedAt'] = pd.to_datetime(df['CreatedAt'], unit='ms')
    date_counts = df.set_index('CreatedAt').resample('M').size()

    #occurrences for each date
    counts = date_counts.values

    fig = px.scatter(df, x=date_counts.index, y=counts, size=counts, color=counts,
                 color_continuous_scale=px.colors.sequential.Rainbow,  range_color=[0, 40], opacity=0.7, hover_data={'count_size': counts}, size_max=20)
    fig.update_layout(xaxis_title='Account Creation Date', yaxis_title='Number of accounts')
    fig.update_traces(marker=dict(line=dict(width=1,color='DarkSlateGrey')))
    
    return fig

def create_wordcount(df):
    all_words = []
    for tweet in df['text']:
        words = tweet.split()
        all_words += [word.lower() for word in words] 
    #remove stopwords
    stop_words = set(stopwords.words('english'))
    query_words = ['see', 'check', 'click','here:',',', '-', 'u','get','go','would','also', 'one', 'know', 'it', 'us','people','time','course,','far','make','need', 'must','always']
    stop_words.update(query_words)
    filtered_words = [word for word in all_words if word not in stop_words]
    #frequency of each word
    freq_dist = nltk.FreqDist(filtered_words)

    n = 40  #words to show
    words, freqs = zip(*freq_dist.most_common(n))
    data = pd.DataFrame({'word': words, 'frequency': freqs})
    fig = px.bar(data, x='word', y='frequency', labels={'word': 'Words', 'frequency': 'Frequency'})

    return fig