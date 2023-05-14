import os
import csv
import nltk
import ast

#function to save data into a csv file in the folder Data/search_terms/file_name.csv
def save_data(data, file_name, search_terms):
    try: # Create directory named after search terms
        os.makedirs("Data/%s" % " ".join(search_terms)) 
        print("Directory created")

    except FileExistsError:
        print("Directory exists")

    #save to csv file
    data.to_csv("Data/%s/%s.csv" %(" ".join(search_terms), file_name))
    
#function to convert csv file into nested list 
#filename should just be Data/search_terms/file_name.csv
def get_data(filename): #assuming that the comments are always the last column
  file = open(filename) #path to csv file
  csvreader = list(csv.reader(file, delimiter=","))
  all_comments = list(x[-1] for x in csvreader[1:]) #create a list containing only the comments without headers
  return all_comments


#function to ensure that search_terms are in product listing
def insearch_result(search_term, title):
    title = title.lower() #as search_term is in lower case
    for keywords in search_term:
        if keywords not in title:
            print(title)
            return False
    return True


#function to tokenise and reduce length of prompt due to token limits
#for openai we use a token limit of 2056 
def tokenised(sentence, maxtoken):
  tokens = nltk.word_tokenize(sentence) #tokenise the sentence into tokens
  max_tokens = maxtoken # set the maximum number of tokens

  #if the sentence has a smaller number of tokens than the maxtoken, nothing will be changed
  truncated_tokens = tokens[:max_tokens] # select the first max_tokens tokens
  truncated_sentence = " ".join(truncated_tokens) # join the tokens back into a sentence
  return truncated_sentence
  
  
