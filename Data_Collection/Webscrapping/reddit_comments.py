#####################################################################################################
# This is the functions to scrape comments about a certain topic from reddit.
# imports:praw, re, pandas, clean and helper functions from Helper.
# Note: This requires you to create a reddit app on https://www.reddit.com/prefs/apps, every app will have an id, stored as reddit_id, and a secret, reddit_secret.
import praw
import re
import pandas as pd
from cleantext import clean
from ...Helper import *

# Main packaged function
# Outputs: Returns a csv with the comments from reddit
# requires: search_terms, number_of_post, reddit_id, reddit_secret


def get_reddit_comments(search_terms, number_of_posts, reddit_id, reddit_secret, create_csv=True):
    search_term = search_terms[0]
    df = scrape_reddit(search_term, number_of_posts, reddit_id, reddit_secret)
    reddit_data = cleanup_reddit(df)
    if create_csv:
        save_data(reddit_data, "reddit", search_terms)
    return reddit_data

# function to search for the comments on reddit threads using the first string in search_terms
# requires: search_term, reddit_id, reddit_secret


def scrape_reddit(search_term, number_of_posts, reddit_id, reddit_secret):
    df = pd.DataFrame(columns=['Posts', 'comments'])
    reddit = praw.Reddit(client_id=reddit_id,
                         client_secret=reddit_secret,
                         user_agent='<console:HAPPY:1.0')
    subreddit = reddit.subreddit(search_term)
    for submission in subreddit.hot(limit=number_of_posts):
        for comment in submission.comments:
            if hasattr(comment, 'body'):
                index = df.shape[0]
                df.loc[index] = [submission.title, comment.body]
    return df

# function to cleanup the reddit comments by removing emojis and splitting them into sentences
# requires: dataframe of comments


def cleanup_reddit(uncleaned_frame):
    df = pd.DataFrame(columns=['Posts', 'comments'])
    uncleaned_frame.reset_index()
    for index, row in uncleaned_frame.iterrows():
        Post, Comment = row['Posts'], row['comments']
        if Comment == "[deleted]":
            continue
        subComments = []
        commented = Comment.split(". ")
        for x in commented:
            subComments.append(x)
        for i in subComments:
            commentina = re.split("[?:!]", i)
            for j in commentina:
                j = clean(j, no_emoji=True)
                if j == "":
                    continue
                index = df.shape[0]
                df.loc[index] = [Post, j]
    return df
