###################################################################################################################################################################
# This is the functions to do sentiment analysis on all the categorised data to help pick the top 5 positive design opportunities and all negative opportunities
# imports: flair, flair.models import TextClassifier, from flair.data import Sentence

####################################################################################################################################################################

from flair.models import TextClassifier
from flair.data import Sentence


#function to sentiment analyse each comment into positive or negative
#using flair as sentiment analysis as it is the most accurate by using text embedding
def sentiment_analysis(prompt):
  classifier = TextClassifier.load('en-sentiment') #loading the model
  sentence = Sentence(prompt) #tokenising sentence
  classifier.predict(sentence) #classifying sentence
  result, confidence = sentence.labels[0].to_dict().values()
  return result, confidence


#function to get design outcomes by comparing how many positive and negative comments are there for each category
#require dictionary input
def positivenegative(dataset):
  negative_cat = []
  positive_cat = []
  category_data = {}

  total_comment = sum([len(x) for x in dataset.values()]) #total number of product reviews
  print(total_comment)
  
  for key in dataset.keys():
    category_data[key] ={}
    negative = 0
    positive = 0
    negative_list = []
    positive_list = []

    for data in dataset[key]:
      result, score = sentiment_analysis(data) #run sentiment analysis through every review and classify
      #print(data, result)
      if result == 'POSITIVE':
        positive += 1 #increase positive comment count
        positive_list.append(data)
      
      elif result == 'NEGATIVE':
        negative += 1 #increase negative comment count
        negative_list.append(data)

    #append the comment to the relevant category under positive comments / negative comments
    #this allow us to look through the data to understand what is the issue behind it
    category_data[key]['negative'] = negative_list 
    category_data[key]['positive'] = positive_list
    
    if positive >= negative: #getting positive design outcomes 
      positive_cat.append([key, positive/total_comment, negative/total_comment])
      print(key, ":positive")

    elif negative > positive: #getting negative design outcomes
      negative_cat.append([key, positive/total_comment, negative/total_comment])
      print(key, ":negative")

  return positive_cat, negative_cat, category_data

#function to get the finalised design outcomes
#require dictionary input
def finalised_design_outcomes(dataset):
  pos_design_outcomes, neg_design_outcomes, categorical_data = positivenegative(dataset)
  sorted_by_neg = sorted(neg_design_outcomes, key=lambda x: x[2], reverse= True)  #sort by negative percentage
  sorted_by_pos = sorted(pos_design_outcomes, key=lambda x: x[1], reverse = True)  #sort by positive percentage

  negative_design_outcomes = sorted_by_neg #get all  negative design outcomes
  positive_design_outcomes = sorted_by_pos[:5] #get top 5 positive design outcomes
  finalised_design_opp = [x[0] for x in negative_design_outcomes] + [x[0] for x in positive_design_outcomes]
  
  return negative_design_outcomes,positive_design_outcomes, finalised_design_opp
  

  
