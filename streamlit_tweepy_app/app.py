from __future__ import unicode_literals
import os
from newsapi_help_func import *
import streamlit as st
import tweepy
import json
import yaml
import operator
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

#Source: https://towardsdatascience.com/how-to-build-your-machine-learning-app-in-3-simple-steps-d56ed910355c
#Source (build with Tweets if time permits): https://medium.com/analytics-vidhya/building-a-twitter-sentiment-analysis-app-using-streamlit-d16e9f5591f8
#Widget Source: https://coinlib.io/widgets?w_chart_coin_id=859&w_chart_pref_coin_id=1505&w_all_theme=Dark#w_chart

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("styles.css")

ticker_html="""
<div style="height:62px; background-color: #1D2330; overflow:hidden; text-align: right; line-height:14px; block-size:62px; font-size: 12px; font-feature-settings: normal; text-size-adjust: 100%; box-shadow: inset 0 -20px 0 0 #262B38;padding:1px;padding: 0px; margin: 0px; width: 100%;"><div style="height:40px; padding:0px; margin:0px; width: 100%;"><iframe src="https://widget.coinlib.io/widget?type=horizontal_v2&theme=dark&pref_coin_id=1505&invert_hover=" width="100%" height="36px" scrolling="auto" marginwidth="0" marginheight="0" frameborder="0" border="0" style="border:0;margin:0;padding:0;"></iframe></div><div style="color: #626B7F; line-height: 14px; font-weight: 400; font-size: 11px; box-sizing: border-box; padding: 2px 6px; width: 100%; font-family: Verdana, Tahoma, Arial, sans-serif;"></div></div>
"""

st.markdown(ticker_html, unsafe_allow_html=True) #Body rendering

st.header("Cryptocurrency News Sentiment Analysis")

st.write("How's Cryptocurrency doing? Enter a coin below")

t = st.text_input("Enter cryptocurrency")

start = st.button("Get Sentiment")

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

    Body_html="""
    <div style="height:560px; background-color: #1D2330; overflow:hidden; text-align: right; line-height:14px; font-size: 12px; font-feature-settings: normal; text-size-adjust: 100%; box-shadow: inset 0 -20px 0 0 #262B38;padding:1px;padding: 0px; margin: 0px; width: 100%;"><div style="height:540px; padding:0px; margin:0px; width: 100%;"><iframe src="https://widget.coinlib.io/widget?type=chart&theme=dark&coin_id=859&pref_coin_id=1505" width="100%" height="536px" scrolling="auto" marginwidth="0" marginheight="0" frameborder="0" border="0" style="border:0;margin:0;padding:0;line-height:14px;"></iframe></div><div style="color: #626B7F; line-height: 14px; font-weight: 400; font-size: 11px; box-sizing: border-box; padding: 2px 6px; width: 100%; font-family: Verdana, Tahoma, Arial, sans-serif;"><a href="https://coinlib.io" target="_blank" style="font-weight: 500; color: #626B7F; text-decoration:none; font-size:11px">Cryptocurrency Prices</a>&nbsp;by Coinlib</div></div>
    """

    st.markdown(Body_html, unsafe_allow_html=True) #Body rendering

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