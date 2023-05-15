#####################################################################################################
# This is the main code file that will immediately run the entire framework
######################################################################################################

#ALL imports
import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import itertools
from langdetect import detect
from cleantext import clean
import time
import googleapiclient.discovery
from youtube_transcript_api import YouTubeTranscriptApi
import os
import csv
import openai
import ast
import nltk
from nltk.tokenize import sent_tokenize
from scipy import spatial 
import gensim.downloader as api
import numpy as np
from transformers import pipeline
import wordninja
from flair.models import TextClassifier
from flair.data import Sentence

from Helper import *
from Data_Collection.Webscrapping.amazon_reviews import *
from Data_Collection.Webscrapping.shopee_reviews import *
from Data_Collection.Webscrapping.youtube_captions import *
from Data_Collection.Webscrapping.youtube_comments import *
from Data_Collection.Design_Opportunities.GPT_keyword import *
from Data_Collection.Design_Opportunities.google_shopping import *

from Data_Cleaning.Keywords_Cleaning import *
from Data_Cleaning.Amazon_Shopee_Cleaning import *
from Data_Cleaning.Shopee_Cleaning import *
from Data_Cleaning.Youtube_Cleaning import *

from Data_Categorisation.Categorisation import *

from Sentiment_Analysis.SentimentAnalysis import *

from Generating_Design_Opportunities.Transcript_Summariser import *
from Generating_Design_Opportunities.Design_Opportunities import *

def Generating_Design_Opportunities(search_terms, ytapi, gpt3api, model="text-davinci-003"):
  #============================================================================================
  #                            DATA COLLECTION webscrapping
  #============================================================================================

  print("Getting Amazon Reviews")
  amazon_data = get_amazon_reviews(search_terms, num_of_links=None, create_csv=True)
  print("Collected", amazon_data.shape[0], "Amazon Reviews")
  amazon_data
        
  print("Getting Shopee Reviews")
  shopee_data = get_all_shopee_reviews(search_terms, num_of_links=None, create_csv=True)
  print("Collected", shopee_data.shape[0], "Shopee Reviews")
  shopee_data
        
  print("Getting Youtube Captions")
  youtube_caption = get_youtube_captions(search_terms, ytapi, count=5, create_csv=True)
  print("Collected Youtube Caption")
  youtube_caption
        
  print("Getting Youtube Comments")
  youtube_comments = get_youtube_comments(search_terms, ytapi, count=5, create_csv=True)
  print("Collected", youtube_comments.shape[0], "Youtube Comments")
  youtube_comments
  
  #============================================================================================
  #                           DATA COLLECTION design keywords
  #============================================================================================

  print("Getting Google Shopping Keywords")
  google_keywords = get_googleshopping_reviews(search_terms, create_csv=True)
  print("There are a total of:", len(google_keywords.keys()), "keywords")
  print(google_keywords)
        
  print("Getting design specifications from GPT-3")
  design_specifications = get_specifications(search_terms, model, gpt3api)
  design_flaws = get_flaws(search_terms, model, gpt3api)
  design_strengths = get_strength(search_terms, model, gpt3api)
  
  total_keywords = total_uncleaned_keywords([google_keywords, design_flaws, design_strengths])
  print("All uncleaned keywords:", total_keywords)
        
  #============================================================================================
  #                                DATA CLEANING keywords
  #============================================================================================
  
  print("Cleaning Keywords")
  final_keywords = creating_keywords(Total_keywords)
  print("Keywords count decreased from", len(Total_keywords), "to", len(final_keywords))
  print("Final keywords", final_keywords)
  
  #============================================================================================
  #                                DATA CLEANING reviews
  #============================================================================================
  
  print("Cleaning Youtube Comments, iteration 1")
  yt_comments = get_data("Data/%s/youtube comments.csv" % " ".join(search_terms))
  yt1 = categorising_comments(yt_comments, 1, search_terms) #categorising comments, model_1
  first_iter = clean_dataset(yt1, search_terms) #clean_dataset to remove irrelevant comments
  first_iter_comments = first_iter['comment'].to_list() #take only the comments and append them to list
  print("Iteration 1 complete, removed", len(yt_comments) - len(first_iter_comments), "irrelevant comments")
  
  print("Cleaning Youtube Comments, iteration 2")
  yt2 = categorising_comments(first_iter_comments, 2, search_terms) #categorising comments, model_2
  final_iter = clean_dataset_2(yt2, search_terms) #clean_dataset again
  final_yt_list = final_iter['comment'].to_list() #final list of comments that are cleaned
  print("Iteration 2 complete, final number of relevant comments:", len(final_yt_list))
  
  print("Cleaning Shopee Reviews")
  shopee_reviews = get_data("Data/%s/shopee reviews.csv" % " ".join(search_terms))
  cleaned_shopee_reviews = cleaning_shopee(shopee_reviews)
  split_cleaned_shopee_reviews = split_sentence(cleaned_shopee_reviews) #split sentence, cleaned_shopee_reviews come from the previous section
  df_3 = categorising_reviews(split_cleaned_shopee_reviews, search_terms) #categorise reviews
  final_shopee = clean_dataset_shopping(df_3, search_terms) #clean reviews
  final_shopee_list = final_shopee['comment'].to_list() #take cleaned comments and put to list
  print("revelant shopee comments from:", len(cleaned_shopee_reviews), "to", len(final_shopee_list))
        
  print("Cleaning Amazon Reviews")
  amazon_reviews = get_data("Data/%s/amazon reviews.csv" % " ".join(search_terms)) #read amazon review file
  split_amazon_reviews = split_sentence(amazon_reviews) #split sentence
  df_4 = categorising_reviews(amazon_reviews,search_terms)  #categorise reviews
  final_amazon = clean_dataset_shopping(df_4, search_terms) #clean reviews
  final_amazon_list = final_amazon['comment'].to_list() #take cleaned comments and put to a list
  print("revelant amazon comments from:", len(amazon_reviews), "to", len(final_amazon_list))

  print("All data cleaned, moving to Data Categorisation")
        
  #============================================================================================
  #                                DATA CATEGORISATION
  #============================================================================================
  
  final_data_list = merging_data(final_yt_list,final_shopee_list,final_amazon_list)
  print("Total Cleaned Data:", len(final_data_list), "reviews and comments")
  
  print("Categorising all Data")
  categorised_comments = categorising_all_data(final_data_list, final_keywords, search_terms, create_csv=True)
  print("Data categorised", categorised_comments)
        
  #============================================================================================
  #                           SENTIMENT ANALYSIS
  #============================================================================================
  
  print("Starting Sentiment Analysis")
  negative_design_outcomes, positive_design_outcomes, finalised_design_opp = finalised_design_outcomes(categorised_comments)
  print("Negative design properties:", negative_design_outcomes)
  print("Positive design properties:", positive_design_outcomes)
  print("Final list of design properties:", finalised_design_opp)
  
  #============================================================================================
  #                           GENERATING DESIGN OPPORTUNITIES 
  #============================================================================================
  
  print("Summarising Youtube Captions")
  youtube_transcripts = get_data("Data/%s/youtube captions.csv" % " ".join(search_terms))
  summarised_reviews = transcript_summariser(youtube_transcripts, search_terms, model, gpt3api)
  print("Summarised youtube captions:", summarised_reviews)
  
  print("Generating Design Opportunities from Youtube Captions")
  generated_design_outcomes = features_extractor(finalised_design_opp, summarised_reviews, model, gpt3api) 
  print("Generated Opportunities:", generated_design_outcomes)
  
  print("Generating Design Opportunities from reviews")
  total_design_opportunities = reviews_design_outcomes(negative_design_outcomes, positive_design_outcomes, categorised_comments, summarised_reviews,search_terms, model, gpt3api)
  print("Total Generated Opportunities", total_design_opportunities)
  
  print("Cleaning and Generating Final set of Design Opportunities")
  final_outcomes = generate_design_outcomes(total_design_opportunities, search_terms, model, gpt3api)
  print("Final Design Opportunities:", final_outcomes)
 
  print("saving data")
  save_txt(final_outcomes, "Design Opportunities" , search_terms)
  print("Complete")


        
        
  
          
        
        
        

  







