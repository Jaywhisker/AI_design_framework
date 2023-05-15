#####################################################################################################
# This is the functions to retrieve comments from Youtube Videos
# imports: googleapiclient.discovery, pandas, clean, helper functions from Helper
import googleapiclient.discovery
import pandas as pd
from cleantext import clean
from ...Helper import *

# Main packaged function
# Outputs: Returns a csv with youtube comments from the videos sweeped based on the search_terms
#        : The function also returns the dataframe itself
# requires: search_terms (list), api_key (string), count (int)


def get_youtube_comments(search_terms, api_key, count=5, create_csv=True):
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
