#####################################################################################################
# This is the functions to remove and clean irrelevant data from youtube comments
# imports: transformers, pipeline, pandas and helper functions from Helper.

######################################################################################################

from transformers import pipeline
import pandas as pd
from ...Helper import *

#=========================================================================================================================================
# 
#                                                     Data Categorising
#                     
#=========================================================================================================================================

#REQUIRES: Data to be in the form of a list, use get_data(filename) from helper function if required
#creating the zeroshot classification model 1 -> the focus of this model would be to try and remove all comments not related to the product vaguely
def cleaning_model_1(prompt, search_terms):
  df = pd.DataFrame(columns = ["comment", "category", "score"])
  pipe = pipeline(model="facebook/bart-large-mnli") #most popular pretrained model
  output = pipe(prompt,
      candidate_labels=["complains about " + " ".join(search_terms),
                        "compliments on " + " ".join(search_terms),
                        "youtube",
                        "questions",
                        "good video reviews",
                        "subscribe to channel",
                        "switching " + " ".join(search_terms),
                        "greetings",
                        "thanks for review",
                        "product shipping",
                        "delivery",
                        "sacarsm of the " + " ".join(search_terms),
                        "suggestion"])
  
  print(output)
  df = df.append({"comment":prompt, "category":output["labels"][0], "score":output["scores"][0]}, ignore_index = True)
  return df


#require data to be in the form of a dataframe 
#due to the large number of labels, the model struggles with some of the comments when they are talking about specific portions of the video but does not mention the product name for the model to catch
def clean_dataset(data, search_terms):
  df = pd.DataFrame(columns = ['comment', 'category', 'score'])  
  for i, rows in data.iterrows():
    cat = rows['category']

    #if the model categorise them as comments related to product append to list of comments
    if cat in ["complains about " + " ".join(search_terms),
               "compliments on " + " ".join(search_terms),
               "sacarsm of the " + " ".join(search_terms)]: 
      df = df.append({"comment": rows['comment'], "category": rows['category'], "score": rows['score']}, ignore_index = True)

    #if the model did not categorise them as comments related to product but have a low confidence level of less than 0.2, this are usually comments that confuse the model 
    #we will append them to the list of comments for further refinement as some of these comments are actually useful (our labels are vague in model 1)
    else:
      if rows['score'] < 0.2: 
        df = df.append({"comment": rows['comment'], "category": rows['category'], "score": rows['score']}, ignore_index = True)
  
  return df

#=========================================================================================================================================
#
#                                                Second Zero Shot
#
#=========================================================================================================================================


#second zeroshot model with more specific labels, mainly taken from the most common design flaws for all products
def cleaning_model_2(prompt, search_terms):
  df = pd.DataFrame(columns = ["comment", "category", "score"])
  pipe = pipeline(model="facebook/bart-large-mnli")
  output = pipe(prompt,
      candidate_labels=["comments about price",
                        "comments about noise",
                        "comments about quality",
                        "reviews on " + " ".join(search_terms),
                        "complains about " + " ".join(search_terms),
                        "compliments on " + " ".join(search_terms),
                        "sacarastic comments",
                        "youtube",
                        "questions",
                        "good video",
                        "links"])
  
  df = df.append({"comment":prompt, "category":output["labels"][0], "score":output["scores"][0]}, ignore_index = True)
  return df

#similar to clean_dataset_1 except cleaning the comments by looking at just the categories this time
def clean_dataset_2(data, search_terms):
  df = pd.DataFrame(columns = ['comment', 'category', 'score'])  
  for i, rows in data.iterrows():
    cat = rows['category']
    score = rows['score']
    #to ensure that we are only taking quality data, we have a minimum threshold score of 0.3
    if cat in ["comments about price", 
               "comments about noise", 
               "comments about quality", 
               "reviews on " + " ".join(search_terms), 
               "complains about " + " ".join(search_terms), 
               "compliments on " + " ".join(search_terms), 
               "sacarastic comments"] and score >=0.3:
      
      df = df.append({"comment": rows['comment'], "category": rows['category'], "score": rows['score']}, ignore_index = True)
  return df

#=========================================================================================================================================
#
#                                               Data Cleaning
#
#=========================================================================================================================================

#categorising comments, require data to be in a list, makes uses of cleaning_model functions
#clean_model to be 1 or 2 depending on which model is used
def categorising_comments(datalist, clean_model, search_terms):
  df = pd.DataFrame(columns = ["comment", "category", "score"])
  for comment in datalist: 
    if clean_model == 1: #if clean_model is 1, means it is first iteration
        try: #try except is to catch if the comment is just a whitespace (will return a no prompt error)
          df = pd.concat([df, cleaning_model_1(comment, search_terms)]) 
        except:
          pass

    elif clean_model == 2: #if clean_model is 2, means its the second iteration
        try:
          df = pd.concat([df, cleaning_model_2(comment, search_terms)])
        except:
          pass
  
  return df


