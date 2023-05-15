#####################################################################################################
# This is the functions to clean all design specifications keywords
# imports: gensim, scipy, numpy and helper functions from Helper.

######################################################################################################

from scipy import spatial 
import gensim.downloader as api
import numpy as np

#function to get all the keywords
#require a list of dictionaries
def total_uncleaned_keywords(data):
    keyword = []
    for i in range(len(data)): 
        for key in data[i].keys(): #getting all the keywords, data[i] must be a dictionary
            keyword.append(key)
    return keyword
 
#standardise data by making all the words lower for the model
def preprocess(s): 
  return [i.lower() for i in s.split()]


#get the vector values of the word in the model (this is used to calculate the cosine similarity)
def get_vector(s, model): 
  return np.sum(np.array([model[i] for i in preprocess(s)]), axis=0)


#every keyword is checked against another keyword for its similarity by checking the cosine similarity of the 2 words
#if the words are different and have a similarity <0.2, append both words into the cleaned_keywords list
def creating_keywords(keywordlist):
  cleaned_keywords = []
  model = api.load("glove-wiki-gigaword-50") #using a smaller model trained on lesser words as the keywords are likely to be common words
  for i in range(len(keywordlist)):   
    for j in range(i, len(keywordlist)): 
      similarity = 1 - spatial.distance.cosine(get_vector(keywordlist[i], model), get_vector(keywordlist[j], model)) 
      if similarity < 0.2:
        cleaned_keywords.append(keywordlist[i])
        cleaned_keywords.append(keywordlist[j])

  cleaned_keywords = list(set(cleaned_keywords)) #remove any duplicated keywords     
  return cleaned_keywords


#limitations: 
#heavily relies on just the OpenAI and google keywords -> OpenAI has a low reproducibility rate and may miss out on certain keywords
#using a small model may have situations where the keywords are not part of the dataset trained for this model -> unable to map the keyword onto the vector space -> error
