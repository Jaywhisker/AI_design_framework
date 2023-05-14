#####################################################################################################
# This is the functions to retrieve the comments from a list of provided articles from the apple insider
# imports: requests, beautifulsoup, pandas and helper functions from Helper.
import requests
from bs4 import BeautifulSoup
import pandas as pd
from ...Helper import *

# Main packaged function
# Outputs: Returns a csv with the comments from the links provided
#        : The function also returns a the dataframe itself
# requires: articles_list ([str])


def get_apple_insider_comments(list_of_articles, create_csv=True):
    if list_of_articles == []:
        list_of_articles = [
            "https://appleinsider.com/articles/23/03/21/iphone-15-mfi-requirements-to-drive-usb-c-charger-demand"]
    apple_insider_data = apple_insider_scraper(list_of_articles)
    if create_csv:
        save_data(apple_insider_data, "apple insider", "articles")
    return apple_insider_data

# function to search through each article in the articles list
# requires: articles_list ([str])


def apple_insider_scraper(list_of_links_to_articles: list[str]):
    df = pd.DataFrame(columns=['Title', 'Comments'])
    for article in list_of_links_to_articles:
        try:
            response = requests.get(article)
            soup = BeautifulSoup(response.content, 'html.parser')
            title = soup.find('h1').text.strip()
            comment_section = soup.find_all(
                'div', {'class': 'col-sm-12 forum-comment'})
            for i in comment_section:
                children = i.findChildren("p", recursive=True)
                commentta = ((children[0].text.strip()))
                index = df.shape[0]
                df.loc[index] = [title, commentta]
                # df = df.append({'title': title, 'comments': commentta},ignore_index=True)
        except:
            print("Something went wrong! Check the link: " + article)
    return df


# Potential function to collect articles of certain product from apple insider
