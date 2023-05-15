#####################################################################################################
# This is the functions to remove and clean irrelevant data from all shopping platforms (Amazona and Shopee in this scenario)
# imports: nltk, transformers, pipeline, pandas and helper functions from Helper.

######################################################################################################

import ntlk
from nltk.tokenize import sent_tokeniz
from transformers import pipeline
import pandas as pd
from ...Helper import *

#function split reviews by sentences such that it is easy to categorise as a review may talk about multiple categories 
#data_list contains alls reviews in a list
def split_sentence(data_list):
  try:
    nltk.download('punkt')
  except:
    pass
  
  comment_list = []
  for data in data_list:
    comment_list.extend(sent_tokenize(data)) #split reviews into sentences and add to comment list

  return comment_list


#zero shot classification focused on delivery and seller
def cleaning_model_shopping(prompt, search_terms):
  df = pd.DataFrame(columns = ["comment", "category", "score"])
  pipe = pipeline(model="facebook/bart-large-mnli") #most popular pretrained model
  output = pipe(prompt,
      candidate_labels=["complains about" + " ".join(search_terms),
                        "compliments on" + " ".join(search_terms),
                        "product bad",
                        "product good",
                        "delivery",
                        "shipping",
                        "seller", 
                        "free",
                        "purchase",
                        "vouchers"])
  
  df = df.append({"comment":prompt, "category":output["labels"][0], "score":output["scores"][0]}, ignore_index = True)
  return df


#cleaning dataset, requires a dataframe input
def clean_dataset_shopping(data, search_terms):
  df = pd.DataFrame(columns = ['comment', 'category', 'score'])  
  for i, rows in data.iterrows():
    cat = rows['category']
    score = rows['score']
    if cat in ["complains about " + " ".join(search_terms), 
               "compliments on " + " ".join(search_terms),
               "product bad",
               "product good"] and score>=0.3: #similar threshold as we want to get a good dataset
      df = df.append({"comment": rows['comment'], "category": rows['category'], "score": rows['score']},ignore_index = True)
  return df


#categorising data, requires list input
def categorising_reviews(datalist, search_terms):
  df = pd.DataFrame(columns = ["comment", "category", "score"])
  for reviews in datalist:
    print(reviews)
    try:
      df = pd.concat([df, cleaning_model_shopping(reviews, search_terms)])
    except:
      pass
  return df
