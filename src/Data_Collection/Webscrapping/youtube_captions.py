#####################################################################################################
# This is the functions to retrieve captions from Youtube Videos.
# imports: googleapiclient.discovery, YouTubeTranscriptApi, pandas, clean, helper functions from Helper.
import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd
from cleantext import clean
from ...Helper import *  # imports the helper functions created in the Helper.py

# Main packaged function
# Outputs: Returns a csv with youtube captions from the videos sweeped based on the search_terms
#        : The function also returns the dataframe itself
# requires: search_terms (list), api_key (string), count (int)


def get_youtube_captions(search_terms, api_key, count=5, create_csv=True):
    youtube = setting_yt(api_key)  # your API key here
    vid_id = youtube_search(search_terms, count, youtube)
    yt_captions = youtube_captions(vid_id, youtube)
    if create_csv:
        save_data(yt_captions, "youtube caption", search_terms)
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
