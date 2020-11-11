# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
import re
import string
import seaborn as sns

analyzer = SentimentIntensityAnalyzer()

# Read your api key environment variable
from newsapi import NewsApiClient
# Init
newsapi = NewsApiClient(api_key='26bfcc03761a4677935c11ba37e48dff')
print(newsapi)

# Fetch the Bitcoin news articles from newsapi
def get_sentiment_scores(text, date, source, url):
    sentiment_scores = {}

    # Sentiment scoring with VADER
    text_sentiment = analyzer.polarity_scores(text)
    sentiment_scores["date"] = date
    sentiment_scores["text"] = text
    sentiment_scores["source"] = source
    sentiment_scores["url"] = url
    sentiment_scores["compound"] = text_sentiment["compound"]
    sentiment_scores["positive"] = text_sentiment["pos"]
    sentiment_scores["neutral"] = text_sentiment["neu"]
    sentiment_scores["negative"] = text_sentiment["neg"]
    if text_sentiment["compound"] >= 0.05:  # Positive
        sentiment_scores["normalized"] = 1
    elif text_sentiment["compound"] <= -0.05:  # Negative
        sentiment_scores["normalized"] = -1
    else:
        sentiment_scores["normalized"] = 0  # Neutral

    return sentiment_scores

def get_sentiments_on_topic(topic):
    """ We loke documentation"""
    sentiments_data = []

    # Loop through all the news articles
    for article in newsapi.get_everything(q=topic, language="en", page_size=100)["articles"]:
        try:
            # Get sentiment scoring using the get_sentiment_score() function
            sentiments_data.append(
                get_sentiment_scores(
                    article["content"],
                    article["publishedAt"][:10],
                    article["source"]["name"],
                    article["url"],
                )
            )

        except AttributeError:
            pass

    return sentiments_data

def sentiment_to_df(sentiments):
    
    # Create a DataFrame with the news articles' data and their sentiment scoring results
    news_df = pd.DataFrame(sentiments)

    # Sort the DataFrame rows by date
    news_df = news_df.sort_values(by="date")

    # Define the date column as the DataFrame's index
    news_df.set_index("date", inplace=True)
    return news_df


# In this section, you will use NLTK and Python to tokenize the text for each coin. Be sure to:
# 1. Lowercase each word
# 2. Remove Punctuation
# 3. Remove Stopwords
# Complete the tokenizer function
# def tokenizer(text):
#     """returns a list of words that is lemmatized, stopworded, tokenized, and free of any non-letter characters. """
#     # Create a list of the words
#     # Convert the words to lowercase
#     # Remove the punctuation
#     # Remove the stop words
#     # Lemmatize Words into root words
#     lemmatizer = WordNetLemmatizer()
#     sw = set(stopwords.words('english'))
#     regex = re.compile("[^a-zA-Z ]")
#     re_clean = regex.sub('', text)
#     words = word_tokenize(re_clean)
#     return [lemmatizer.lemmatize(word.lower()) for word in words if word.lower() not in set(stopwords.words('english'))]

# # Text preprocessing steps - remove numbers, captial letters and punctuation
# def preprocess_sentiment(df):
#     alphanumeric = lambda x: re.sub('\w*\d\w*', ' ', x)
#     punc_lower = lambda x: re.sub('[%s]' % re.escape(string.punctuation), ' ', x.lower())

#     df['tokens'] = df.text.map(alphanumeric).map(punc_lower)
#     # only comparing positive and negative; took out neutral because logistic regression requires 2 inputs
#     df['sentiment'] = df[['positive','negative']].idxmax(1)