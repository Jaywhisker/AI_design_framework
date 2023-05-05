#####################################################################################################
# This is the functions to retrieve captions from Youtube Videos
# imports: googleapiclient.discovery, YouTubeTranscriptApi, pandas, clean, helper functions from Helper
import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
from cleantext import clean
from Helper import *  # imports the helper functions created in the Helper.py

# Main packaged function
# Outputs: Returns a csv with youtube captions from the videos sweeped based on the search_terms
#        : The function also returns the dataframe itself
# requires: search_terms (list), api_key (string), count (int)
def get_youtube_captions(search_terms, api_key, count, create_csv=True):
    youtube = setting_yt(api_key)  # your API key here
    vid_id = youtube_search(search_terms, count, youtube)
    yt_captions = youtube_captions(vid_id, youtube)
    if create_csv:
        save_data(yt_captions, "youtube transcript", search_terms)
    return yt_captions

# function to access youtube with API key
def setting_yt(Api_key):
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=Api_key)
    return youtube


# function to search on youtube
# requires: search term, maximum number of youtube results (assuming <=50), access to youtube api key
def youtube_search(search_term, maxresults, youtube):
    vidID = []  # container for video ids

    # search for youtube results and get back the video ID
    print("Searching for videos")
    request = youtube.search().list(
        q=" ".join(search_term),
        part="id",
        type="video",
        maxResults=maxresults)

    search_response = request.execute()

    # getting the videoID and appending them to the container
    for i in range(maxresults):
        videoID = search_response['items'][i]['id']["videoId"]
        vidID.append(videoID)

    return vidID


# function to get youtube video titles
# require a list of video ids
def get_title(vid_id, youtube):

    # accessing youtube video data by searching based on the video id
    request = youtube.videos().list(
        part="snippet, statistics",
        id=vid_id)

    # execute search and get video information
    video_response = request.execute()
    title = video_response['items'][0]['snippet']['title']  # extract title

    # we are also returning video_response (contains video information) as we will need it to get video_comments
    return title, video_response


# function to get youtube transcript
# requires a list of video ids
def youtube_captions(vidID, youtube):
    df = pd.DataFrame(columns=['title', 'caption'])

    # iterate through every video
    for i in range(len(vidID)):
        try:
            # access the youtube transcript, captions will return a list of dictionary with the following output: [{'text': 'captions', 'start': start time, 'end': end time}]
            captions = YouTubeTranscriptApi.get_transcript(vidID[i])
            cleaned_captions = ""

            # get video title as well
            title, video_response = get_title(vidID[i], youtube)

            for text in captions:
                if text["text"] == "[MUSIC]":  # if the caption is music ignore
                    pass

                elif text["text"] == " ":  # if no caption also ignore
                    pass

                else:
                    cleaned_captions += text['text'].strip()
                    cleaned_captions += " "

            # limitations: as the captions do no include punctuation, the transcript will also NOT include punctuations
            # store caption into datfram
            df = df.append(
                {"title": title, "caption": cleaned_captions}, ignore_index=True)

        except:
            pass

    return df

#####################################################################################################
# This is the functions to retrieve captions from Youtube Videos
# imports: googleapiclient.discovery, pandas, clean, helper functions from Helper
import googleapiclient.discovery
import pandas as pd
from cleantext import clean
from Helper import *

# Main packaged function
# Outputs: Returns a csv with youtube comments from the videos sweeped based on the search_terms
#        : The function also returns the dataframe itself
# requires: search_terms (list), api_key (string), count (int)
def get_youtube_comments(search_terms, api_key, count, create_csv=True):
    # your API key here
    youtube = setting_yt(api_key)
    vid_id = youtube_search(search_terms, count, youtube)
    yt_comments = youtube_comments(vid_id, youtube)
    if create_csv:
        save_data(yt_comments, "youtube comments", search_terms)
    return yt_comments


# function to access youtube with API key
def setting_yt(Api_key):
    api_service_name = "youtube"
    api_version = "v3"
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey=Api_key)
    return youtube

# function to search on youtube
# requires: search term, maximum number of youtube results (assuming <=50), access to youtube api key
def youtube_search(search_term, maxresults, youtube):
    vidID = []  # container for video ids

    # search for youtube results and get back the video ID
    print("Searching for videos")
    request = youtube.search().list(
        q=" ".join(search_term),
        part="id",
        type="video",
        maxResults=maxresults)

    search_response = request.execute()

    # getting the videoID and appending them to the container
    for i in range(maxresults):
        videoID = search_response['items'][i]['id']["videoId"]
        vidID.append(videoID)

    return vidID

# function to get all comments in the video
# requires: comment_reponse, title of video, dataframe (will append on given dataframe)
def get_all_comments(response, title, df):
    for comment in response['items']:
        # obtain main comments
        comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
        # clean to remove emojis
        comment_text = clean(comment_text, no_emoji=True)
        # get like count
        likes_count = comment['snippet']['topLevelComment']['snippet']['likeCount']

        if 'replies' in comment.keys():  # if main comments have replies
            for reply in comment['replies']['comments']:
                rtext = reply['snippet']['textDisplay']  # obtain reply
                rtext = clean(rtext, no_emoji=True)  # clean to remove emojis
                rlike = reply['snippet']['likeCount']  # get like count
                # append replies to data
                df = df.append({"title": title, "likes": rlike,
                               "comments": rtext, }, ignore_index=True)

        # ignoring the structure between replies and comments as data cleaning will only take relevant comments afterwards
        df = df.append({"title": title, "likes": likes_count, "comments": comment_text},
                       ignore_index=True)  # append main comment to data
    return df


# function to get youtube video titles
# require a list of video ids
def get_title(vid_id, youtube):

    # accessing youtube video data by searching based on the video id
    request = youtube.videos().list(
        part="snippet, statistics",
        id=vid_id)

    # execute search and get video information
    video_response = request.execute()
    title = video_response['items'][0]['snippet']['title']  # extract title

    # we are also returning video_response (contains video information) as we will need it to get video_comments
    return title, video_response


# function to get all comments and likes
# requires a list of video IDs
def youtube_comments(vidID, youtube):
    df = pd.DataFrame(columns=['title', 'likes', 'comments'])

    for i in range(len(vidID)):  # iterate through every video id

        # get_title will already run the video and get the video_data under video_response
        title, video_response = get_title(vidID[i], youtube)

        try:  # use try/except to check if comments exists
            comment_count = video_response['items'][0]['statistics']['commentCount']
            print("Video-", title, "-- Comment count: ", comment_count)

            # request for comment
            request_comment = youtube.commentThreads().list(
                part="snippet, replies",
                videoId=vidID[i])
            comment_response = request_comment.execute()

            # run get_all_comments to get all the comments
            df = get_all_comments(comment_response, title, df)

            nextpg = comment_response.get("nextPageToken", "nil")

            while nextpg != 'nil':  # load next page of comments
                next_page_ = comment_response.get(
                    'nextPageToken')  # new request for next page
                request = youtube.commentThreads().list(
                    part="snippet,replies",
                    pageToken=next_page_,
                    videoId=vidID[i]
                )
                comment_response = request.execute()

                # run get_all_comments to get all the comments
                df = get_all_comments(comment_response, title, df)
                # check if there is a next page of comments
                nextpg = comment_response.get('nextPageToken', 'nil')

        except:
            # when comments are turned off
            print("Video", i + 1, "-", title,
                  "-- Comments are turned off, ignoring video")

    return df

#####################################################################################################
# This is the functions to retrieve the keywords that google shopping has classified the comments for a product into
# imports:beautifulSoup, selenium, time, pandas and helper functions from Helper
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from Helper import *

# Main packaged function
# Outputs: Returns a csv with the title that the keyword came from, number of reviews, the keyword, and the percentage that are either positive or negative comments
#        : The function also returns a dictionary of the keywords after any repetitions have been removed.
# requires: search_terms (list)
def get_googleshopping_reviews(search_terms, create_csv=True):
    product_ids = googleshopping_search(search_terms)
    google_data, google_data_dictionary = googleshopping_keywords(
        product_ids, search_terms)
    # saving data
    if create_csv:
        save_data(google_data, "google shopping", search_terms)
    return google_data_dictionary


# function to search on google shopping using selenium (very similar to shopee)
# requires: insearch_result() function, search terms
def googleshopping_search(search_terms):
    base_url = "https://shopping.google.com/"

    # initialising chrome and going to the url
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(base_url)

    # finding search bar and searching for search_terms
    search = driver.find_element("xpath", "//*[@id='REsRA']")
    print("The input Element is: ", search)
    search.send_keys(" ".join(search_terms))
    search.send_keys(Keys.RETURN)

    # pausing to let the page load and scrape the page html
    time.sleep(5)
    page = driver.page_source

    # close the driver
    time.sleep(2)
    driver.close()

    # parse the page with beautiful soup
    soup = BeautifulSoup(page, "html.parser")
    product_id = []  # container to hold all the product id

    # get every link in the search result
    for links in soup.find_all('a', href=True):
        # some of the links are advertisments, ignore if they are not google shopping products
        if "/shopping/product" in links['href']:
            # get product id
            end_index = links['href'].index("?")
            id = links['href'][18:end_index]

            # ensure product id is unique as google shopping has multiple listing to the same product
            if id not in product_id:
                product_id.append(id)

    return product_id


# function to obtain the summarised keywords in google_shopping
# requires: list of google shopping product id
def googleshopping_keywords(productID, search_terms):

    # creating the storing varirables
    df = pd.DataFrame(columns=["Title", "Number of Reviews",
                      "Keywords", "Percentage", "Positive/Negative"])
    keyword_dict = {}
    reviewcatchingbin = []

    # base_url
    base_url = "https://www.google.com/shopping/product/"

    for i in range(len(productID)):
        # when there is /offers, it affects getting to the product so we have to cut the /offers in productID
        if "/offers" in productID[i]:
            index = productID[i].index("/offers")
            productID[i] = productID[i][:index]

        # getting product review links
        url = base_url + productID[i] + "/reviews"
        print(url)

        # using selenium to open the website due to same reason as shopee
        driver = webdriver.Chrome("chromedriver.exe")
        driver.get(url)

        # let page load before taking the html source code
        time.sleep(5)
        page = driver.page_source
        time.sleep(2)

        # close the driver
        driver.close()

        # parse the page to get the title, anyreviews, numreviews
        soup = BeautifulSoup(page, 'html.parser')
        title = soup.find("div", {"class": "f0t7kf"}).text
        anyreviews = soup.find("div", {"class": "rktlcd"})
        numreviews = soup.find("span", "HiT7Id").text
        print(numreviews)

        # if there are no reviews for the product, anyreviews will return None
        if anyreviews == None:
            print("No reviews found")
            pass

        # some product have different ID but look at the same reviews (this is due to different products that have different listing for different colours)
        # to prevent repeated data, ignore the reviews
        elif numreviews in reviewcatchingbin:
            print("repeated review")
            pass

        else:
            # checking if the product name is accurate
            intitle = insearch_result(search_terms, title)
            # add the number of reviews into review catching bin
            reviewcatchingbin.append(numreviews)

            if intitle:
                for span in soup.find_all("span", "QIrs8"):
                    text = span.text
                    if text == "Select to view all reviews":  # ignore first text in this span
                        pass

                    # data will be in the format of: View xx reviews about 'keyword'. xx% of the reviews are 'positive/negative'.
                    else:
                        reviews_index = text.index("r")
                        about_index = text.index("about")
                        full_stop_index = text.index(".")
                        percentage_index = text.index("%")

                        # slicing View xx r -> xx
                        num_of_reviews = text[4: reviews_index].strip()
                        # slicing about 'keyword'. -> keyword
                        keywords = text[about_index +
                                        len("about")+1: full_stop_index]
                        percentage = text[full_stop_index +
                                          2: percentage_index]  # . xx% -> xx
                        positivenegative = text[-9:-1]  # positive / negative

                        keyword_dict[keywords] = positivenegative
                        df = df.append({"Title": title, "Number of Reviews": num_of_reviews, "Keywords": keywords,
                                       "Percentage": percentage, "Positive/Negative": positivenegative}, ignore_index=True)
    print(df)

    # returning dictionary because total_uncleaned_keywords() requires dictionary
    return df, keyword_dict
#####################################################################################################
# This is the functions to scrape comments about 
# imports:praw, re, pandas, clean and helper functions from Helper
# Note: This requires you to create a reddit app on https://www.reddit.com/prefs/apps, every app will have an id, stored as reddit_id, and a secret, reddit_secret.
import praw
import re
import pandas as pd
from cleantext import clean
from Helper import *

# Main packaged function
# Outputs: Returns a csv with the comments from reddit
# requires: search_terms, number_of_post, reddit_id, reddit_secret 
def get_reddit_comments(search_terms, number_of_posts, reddit_id, reddit_secret):
    search_term = search_terms[0]
    df = scrape_reddit(search_term,number_of_posts, reddit_id, reddit_secret)
    reddit_data = cleanup_reddit(df)
    if create_csv:
        save_data(reddit_data, "reddit", search_terms)
    return reddit_data    

# function to search for the comments on reddit threads using the first string in search_terms
# requires: search_term, reddit_id, reddit_secret
def scrape_reddit(search_term, number_of_posts,reddit_id,reddit_secret):
    df = pd.DataFrame(columns=['Posts', 'Comments'])
    reddit = praw.Reddit(client_id=reddit_id,
                         client_secret=reddit_secret,
                         user_agent='<console:HAPPY:1.0')
    subreddit = reddit.subreddit(search_term)
    for submission in subreddit.hot(limit=number_of_posts):
        for comment in submission.comments:
            if hasattr(comment,'body'):
                index = df.shape[0]
                df.loc[index] = [submission.title, comment.body]
    return df

# function to cleanup the reddit comments by removing emojis and splitting them into sentences
# requires: dataframe of comments
def cleanup_reddit(uncleaned_frame):
    df = pd.DataFrame(columns=['Posts', 'Comments'])
    uncleaned_frame.reset_index()
    for index, row in uncleaned_frame.iterrows():
        Post, Comment = row['Posts'], row['Comments']
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
