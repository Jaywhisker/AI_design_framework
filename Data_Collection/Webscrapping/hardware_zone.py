#####################################################################################################
# This is the functions to retrieve the comments about the iphone from hardwarezone's dedicated page
# the iphone chat room
# imports:beautifulSoup, selenium, time, pandas, clean and helper functions from Helper.
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
from cleantext import clean
from ...Helper import *


# Main packaged function
# Outputs: Returns a csv with the comments from the various pages scanned
#        : The function also returns a the dataframe itself
# requires: number_of_pages (int)
def get_hardware_zone_comments(number_of_pages, create_csv=True):
    df = search_hardware_zone_forum("iphone", number_of_pages)
    hardware_zone_data = clean_hardware_zone(df)
    if create_csv:
        save_data(hardware_zone_data, "hardware zone", "iphone")
    return hardware_zone_data

# function to generate the number of pages to scan on the forum
# requires: basic_link (str), count(int)


def generate_links_hardware_zone(basic_link, count):
    listed = []
    for i in range(count):
        listed.append(basic_link + 'page-' + str(i))
    return listed

# function to collect the comments from the various pages on the forum
# requires: main_keyword (set as 'iphone') and number_of_pages (int)


def search_hardware_zone_forum(main_keyword, number_of_pages):
    basiclink = 'https://forums.hardwarezone.com.sg/forums/the-iphone-chat-room.240/'
    links = generate_links_hardware_zone(basiclink, number_of_pages)
    options = webdriver.ChromeOptions()
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options)

    list_links = []
    for link in links:
        driver.get(link)
        htmlsource = driver.page_source
        driver.quit()
        time.sleep(5)
        soup = BeautifulSoup(htmlsource, 'html.parser')
        posts = soup.find_all('div', {'class': 'structItem--thread'})
        for post in posts:
            posted = post.find('div', {'class': 'structItem-title'})
            info = post.find('div', {'class': 'structItem-cell--meta'})
            linkedin = posted.findChildren("a", recursive=True)
            try:
                link_to_thread = (linkedin[0]['href'])
                numberofposts = info.findChildren(
                    "a", recursive=True, href=True)[0].text.strip()
                link_to_thread = "https://forums.hardwarezone.com.sg" + link_to_thread
                if main_keyword in link_to_thread:
                    list_links.append([link_to_thread, numberofposts])
            except:
                print('no link found or cannot find number of replies')

    for listed_link in list_links:
        link = listed_link[0]
        options = webdriver.ChromeOptions()
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get(link)
        htmlsource = driver.page_source
        time.sleep(5)
        driver.quit()
        time.sleep(10)
        soup = BeautifulSoup(htmlsource, 'html.parser')
        pageNav = soup.find_all('li', {'class': 'pageNav-page'})
        CommentPageList = []
        try:
            lastpage = pageNav[-1]
            count = int(lastpage.findChildren(
                'a', recursive=True)[0].text.strip())
            pages = 5
            # if managed to find the number of pages per forum sheet,
            # then add the number of pages into the list starting from the back
            while count > 0 and pages > 0:
                new_link = link + 'page-' + str(count)
                CommentPageList.append([link, count, new_link])
                pages -= 1
                count -= 1

        except:
            # ok so only one page
            print('Could not find pageNav')
            new_link = link + 'page-' + str(1)
            CommentPageList.append([link, 1, new_link])

    df = pd.DataFrame(columns=["Forum Link", "Page count", "Comments"])
    for yesnt in CommentPageList:
        options = webdriver.ChromeOptions()
        options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        unnecessary, Page_number, Link = yesnt[0], yesnt[1], yesnt[2]
        driver.get(Link)
        time.sleep(3)
        htmlsource = driver.page_source
        driver.quit()
        time.sleep(5)
        soup = BeautifulSoup(htmlsource, 'html.parser')
        responses = soup.find_all('div', {'class': 'bbWrapper'})
        for response in responses:
            df.loc[len(df)] = {"Forum Link": clean(
                Link, no_emoji=True), "Page count": Page_number, "Comments": response.text.strip()}
    return df


# function to obtain the summarised keywords in google_shopping
# requires: dataframe of comments
def clean_hardware_zone(dataframe):
    df = pd.DataFrame(columns=["comments"])
    for row in dataframe.iterrows():
        sentence = row[-1]
        if "Click to expand..." in sentence:
            slicing_index = sentence.index("Click to expand...") + 18
        else:
            slicing_index = 0
        sentence = (sentence[slicing_index:].strip())
        df.loc[len(df)] = {"comments": sentence}

    return df
