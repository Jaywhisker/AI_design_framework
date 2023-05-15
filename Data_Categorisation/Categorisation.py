#####################################################################################################
# This is the functions to categorise the data based on the cleaned keywords 
# imports: transformers, pipeline, pandas and helper functions from Helper.

######################################################################################################
from transformers import pipeline
import pandas as pd
from ...Helper import *

#function to merge all 3 data into a singular list
#requires all inputs to be a list
def merging_data(youtube_comment, shopee_reviews, amazon_reviews):
  merged_data =  youtube_comment + shopee_reviews + amazon_reviews
  return merged_data


#function to categorise one comment into the respective keywords from design outcomes
#input: prompt = comment, keywords = final list of keywords, dictionary = {} which will hold categorised_comments
def categorising_single_data(prompt, keywords, dictionary):
  pipe = pipeline(model="facebook/bart-large-mnli") #most popular pretrained model
  output = pipe(prompt,
      candidate_labels=keywords)  
  i = 0
  #have a minimum score catching as there are some comments that are not related to product that failed the cleaning 
  while output['scores'][i] > 0.35: #as comments can be talking about different parts of the product which involves multiple categories      
    dictionary[output["labels"][i]].append(prompt) #update the comment in the dictionary for that category, dictionary[key] must be a list 
    i += 1
  return dictionary #returns updated dictionary


#function to categorise all comments, return both dictionary and dataframe such that dataframe can be save if wanted
def categorising_all_data(all_data, all_keywords, search_terms, create_csv=True):
  categorised_comments  = {}
  for keyword in all_keywords: #creating the categorised comments dictionary
    categorised_comments[keyword] = [] #dictionary values will be a list to hold all the comments
    
  #iterate through every comment in final_data_list
  for data in all_data:
    categorised_comments = categorising_data(data, final_keywords, categorised_comments)
  print(categorised_comments)
  
  #saving categorised_comments to a csv file just in case
  if create_csv:
    df_all = pd.DataFrame(columns=['Comments', 'Category']) #create a datafram object
    for key in categorised_comments.keys():
      value = categorised_comments[key] #comments [] for all comments related to category
      for comments in value:
        df_all = df_all.append({'Comments': comments, 'Category': key}, ignore_index = True) #append each commment into df
    save_data(df_all, "categorised data", search_terms)
      
 return categorised_comments

  
  
