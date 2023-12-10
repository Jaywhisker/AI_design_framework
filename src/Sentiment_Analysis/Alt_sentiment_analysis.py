#####################################################################################################
# These are functions that are used in the Alt.py file
######################################################################################################

import string
from transformers import pipeline

import pandas as pd
import os


def sentiment_labeller(df, categories):
    sentiment_pipeline = pipeline("sentiment-analysis")

    sentences = []
    for index, row in df.iterrows():
        sentence, category = row['Comments'], row['label']
        sentences.append(sentence)

    # Takes the labels positive and negative and adds it as a new column to the dataframe supplied
    new_list = list(map(lambda x: x['label'], sentiment_pipeline(sentences)))
    df['Sentiment'] = new_list

    # Now create the stuff to store the things in
    # postive_word_storage is the compliments in the category
    # negative_word_storage is the complains in the category
    # storage is just the score
    storage = {}
    positive_word_storage = {}
    negative_word_storage = {}
    for x in categories:
        storage[x] = 0
        positive_word_storage[x] = ""
        negative_word_storage[x] = ""

    # iterate through all the rows
    for index, row in df.iterrows():
        comment = row['Comments']
        category = row['label']
        positiveNegative = row['Sentiment']
        active = None
        if category in categories:
            if positiveNegative == "POSITIVE":
                storage[category] += 1
                active = positive_word_storage
            else:
                storage[category] -= 1
                active = negative_word_storage
            comment = comment.strip()
            if comment[-1] in string.punctuation:
                active[category] = active[category] + comment
            else:
                active[category] = active[category] + comment + '.'
        Qualatative = sorted(list(storage.items()),
                             key=lambda x: abs(x[1]), reverse=True)
    return Qualatative, positive_word_storage, negative_word_storage
# Quantitative data analysed, now go find the largest numerical category and if they are good or bad
