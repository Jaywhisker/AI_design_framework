#####################################################################################################
# This is the function to clean Shopee reviews by removing merged words
# imports: transformers, pipeline, wordninja, pandas and helper functions from Helper.

######################################################################################################

import wordninja
from transformers import pipeline
import pandas as pd
from ...Helper import *


#remove performance, best features and value for money for zero shot
def cleaning_shopee(data):
  reviews =[]
  for x in data:
    indexes = []
    for idx in range(len(x)): #finding all the : indexes
      if x[idx] == ":":
        indexes.append(idx)
    
    #section is cleaning the shopee comments to remove performance: xxxbest feature(s): xxxvalue for money: xxx
    try:
      edited_reviews = x[indexes[-1] + 2:] #removing until last semicolon which is for the performance, best features / value for money
      for words in edited_reviews.split(): #as there is no space between the value for money: xxxReview, check the first word to remove the xxx such that we can get Review
        #Eg. Value for money: not baddelivery -> wordninja = [bad, delivery], get index of delivery and slice sentence right before delivery
        is_word = wordninja.split(words) 
        if len(is_word) != 1: #we are at xxxReviews part of the comment as there is 2 words
          index = edited_reviews.index(is_word[0])  
          edited_reviews = edited_reviews[index + len(is_word[0]):] #cut the string the moment of the second yes
          break
      print(edited_reviews)
      reviews.append(edited_reviews)
   
    except: #no semicolon which means review does not have performance, best features or value for money
      reviews.append(x)

  return reviews  


