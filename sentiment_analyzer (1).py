# -*- coding: utf-8 -*-
"""Sentiment Analyzer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/17LjNQUcRE1FJZoif3pOpaOkh_OT9jQ_0
"""

import numpy as np
import pandas as pd

data=pd.read_csv("set1(1).csv")
data

from nltk.corpus import stopwords

import re
import nltk
from nltk.stem import PorterStemmer
# Manually define stopwords
stop_words = set([
    'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're",
    "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he',
    'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's",
    'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which',
    'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was',
    'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did',
    'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while',
    'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through',
    'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out',
    'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
    'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some',
    'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can',
    'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y',
    'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't",
    'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't",
    'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't",
    'won', "won't", 'wouldn', "wouldn't"
])

# Initialize Porter Stemmer
stemmer = PorterStemmer()
# Assuming 'data' is your DataFrame and it has a column named 'text'
def Clean(Text):
    sms = re.sub("[^a-zA-Z]", " ", str(Text))
    sms = sms.lower()
    sms = sms.split()
    sms = [word for word in sms if word not in stop_words]  # Remove stopwords
    sms = [stemmer.stem(word) for word in sms]  # Stem words
    sms = " ".join(sms)
    return sms

data["Clean_Text"] = data["text"].apply(Clean)
# Printing the first 5 cleaned texts
print("The first 5 Texts:", *data["Clean_Text"][:100], sep="\n")

import matplotlib.pyplot as plt
from collections import Counter
# Assuming 'data' is your DataFrame and it has a column named 'Clean_Text'
all_text = ' '.join(data["Clean_Text"])
# Count the frequency of each word
word_counts = Counter(all_text.split())
# Get the top 10 most common words
top_words = word_counts.most_common(10)
words, counts = zip(*top_words)
# Plotting
plt.figure(figsize=(10, 6))
plt.bar(words, counts, color='skyblue')
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.title('Top 10 Most Frequent Words After Text Cleaning')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

data["Clean_Text"].fillna("", inplace=True)

from textblob import TextBlob
# Assuming 'data' is your DataFrame and it has a column named 'Clean_Text'
data["Clean_Text"] = data["text"].apply(Clean)
# Perform sentiment analysis using TextBlob
sentiments = []
for text in data["Clean_Text"]:
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        sentiments.append("positive")
    elif sentiment < 0:
        sentiments.append("negative")
    else:
        sentiments.append("neutral")
# Count the sentiment labels
sentiment_counts = pd.Series(sentiments).value_counts()
plt.figure(figsize=(8, 5))
sentiment_counts.plot(kind='bar', color=['green', 'red', 'blue'])
plt.title('Sentiment Analysis using TextBlob')
plt.xlabel('Sentiment')
plt.ylabel('Count')
plt.xticks(rotation=0)
plt.show()

positive_words = []
# Analyze the polarity of each word in the cleaned text
for text in data["Clean_Text"]:
    # Tokenize the text by splitting on whitespace
    words = text.split()
    for word in words:
        word_polarity = TextBlob(word).sentiment.polarity
        if word_polarity > 0:
            positive_words.append(word.lower())  # Append positive word to the list
# Convert the list of positive words to a Series and count the occurrences
positive_word_counts = pd.Series(positive_words).value_counts()
# Get the top 10 most frequent positive words
top_positive_words = positive_word_counts.head(10)
# Generate colors for the bars
num_bars = len(top_positive_words)
colors = plt.cm.tab10(np.linspace(0, 1, num_bars))
if not top_positive_words.empty:
    plt.figure(figsize=(10, 6))
    top_positive_words.plot(kind='bar', color=colors)
    plt.title('Top 10 Most Frequent Positive Words')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.show()
else:
    print("No positive words found.")

positive_words = []
negative_words = []
neutral_words = []
for text in data["Clean_Text"]:
    words = text.split()
    for word in words:
        word_polarity = TextBlob(word).sentiment.polarity
        if word_polarity > 0:
            positive_words.append(word.lower())  # Append positive word to the list
        elif word_polarity < 0:
            negative_words.append(word.lower())  # Append negative word to the list
        else:
            neutral_words.append(word.lower())  # Append neutral word to the list
positive_word_counts = pd.Series(positive_words).value_counts()
negative_word_counts = pd.Series(negative_words).value_counts()
neutral_word_counts = pd.Series(neutral_words).value_counts()
top_neutral_words = neutral_word_counts.head(10)
num_bars = len(top_neutral_words)
colors = plt.cm.tab10(np.arange(num_bars))
plt.figure(figsize=(10, 6))
top_neutral_words.plot(kind='bar', color=colors)
plt.title('Top 10 Most Frequent Neutral Words')
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.xticks(rotation=45)
plt.show()

positive_words = []
negative_words = []
for text in data["Clean_Text"]:
    words = text.split()
    for word in words:
        word_polarity = TextBlob(word).sentiment.polarity
        if word_polarity > 0:
            positive_words.append(word.lower())
        elif word_polarity < 0:
            negative_words.append(word.lower())
print("Negative words found:")
print(negative_words)
negative_word_counts = pd.Series(negative_words).value_counts()
# Plotting the most frequent negative words
if not negative_word_counts.empty:
    plt.figure(figsize=(10, 6))
    negative_word_counts.head(10).plot(kind='bar', color='red')
    plt.title('Top 10 Most Frequent Negative Words')
    plt.xlabel('Words')
    plt.ylabel('Frequency')
    plt.xticks(rotation=45)
    plt.show()
else:
    print("No negative words found.")