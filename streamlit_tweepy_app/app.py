from __future__ import unicode_literals
import os
from newsapi_help_func import *
import streamlit as st
import tweepy
import json
import yaml
import operator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

st.header("Cryptocurrency News Sentiment Analysis")

st.write("Enter the cryptocurrency coin you want to check the sentiment for. A selection of news articles will appear. Press the stop button in right hand corner to stop the streaming. Press the reset button to reset to the starting screen.")

t = st.text_input("Enter cryptocurrency")

start = st.button("Get Sentiment")

stop = st.button("Reset")

analyser = SentimentIntensityAnalyzer()

if start:
    crypto_sentiment = get_sentiments_on_topic(str(t))
    crypto_df = sentiment_to_df(crypto_sentiment)
    compound_score = crypto_df.describe().loc['mean']['compound']

    st.write('Sentiment Score: ', compound_score)
    if compound_score >= 0.05:  # Positive
        st.write('The sentiment score is above 0.05. Things are looking pretty positive')
        st.write("Long-Term Investors: HODL")
        st.write("Day Traders: Sell")
    elif compound_score <= -0.05:  # Negative
        st.write("The sentiment score is below -0.05. Things are looking negative")
        st.write("Long-Term Investors: Buy")
        st.write("Day Traders: Buy")
    else:
        st.write("The sentiment score is in betwee -0.05 and 0.05. Just hang tight")
    
    st.write(crypto_df.head()[['text','source','url']])

# class StreamListener(tweepy.StreamListener):
    
#     def on_status(self, status):
#         if not stop:
#             if hasattr(status, "retweeted_status"):
#                 pass
#             else:
#                 try:
#                     text = status.extended_tweet["full_text"]
#                     score = analyser.polarity_scores(text)
#                     st.write(text)
#                     m = max(score.items(), key=operator.itemgetter(1))[0]
#                     if m == 'neg':
#                         st.error("The sentiment is: {}".format(str(score)))
#                     elif m == 'neu':
#                         st.warning("The sentiment is: {}".format(str(score)))
#                     elif m == 'pos':
#                         st.success("The sentiment is: {}".format(str(score)))
#                     else:
#                         st.info("The sentiment is: {}".format(str(score)))
#                 except AttributeError:
#                     text = status.text
#                     score = analyser.polarity_scores(text)
#                     st.write(text)
#                     m = max(score.items(), key=operator.itemgetter(1))[0]
#                     if m == 'neg':
#                         st.error("The sentiment is: {}".format(str(score)))
#                     elif m == 'neu':
#                         st.warning("The sentiment is: {}".format(str(score)))
#                     elif m == 'pos':
#                         st.success("The sentiment is: {}".format(str(score)))
#                     else:
#                         st.info("The sentiment is: {}".format(str(score)))
#             return True
#         else:
#             exit()
#             return False
        

# def stream_tweets(tag):
#     listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True, wait_on_rate_limit_notify=True))
#     streamer = tweepy.Stream(auth=auth, listener=listener, tweet_mode='extended')
#     query = [str(tag)]
#     streamer.filter(track=query, languages=["en"])
    
# if start:
#     stream_tweets(str(t))