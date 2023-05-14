#####################################################################################################
# This is the functions to summarise youtube transcript
# imports: ast, open ai and helper functions from Helper.

######################################################################################################

import openai
from ...Helper import *

#function to summarise one youtube transcript into its pros and cons
#require: data is a singular paragraph containing the youtube transcript to summarise
def single_transcript_summariser(data, search_terms, apikey):
  openai.api_key = apikey
  prompt = "Summarise the flaws and strengths of the" + " ".join(search_terms) + ":" + data
  model = "text-davinci-003" #GPT-3 model name
  summary = generate_text(prompt, model)
  return summary

#function to summarise all youtube transcripts into its pros and cons
#require: nested list of paragraph containing each youtube transcript
def transcript_summariser(youtube_transcript, search_terms, apikey):
  for transcripts in youtube_transcripts:
  result = transcript_summariser(transcripts, search_terms)
  summarised_reviews += result.strip() #remove whitespace 
  return summarised_reviews


#function to summarise the opinions of each category for the product based on the youtube transcript summary
#require: finalised design outcomes keywords, data = singular paragraph containing summarised youtube transcript 
def features_extractor(categories, data, apikey):
  openai.api_key = apikey
  prompt = "based on this paragraph:" + data + "\n summarise why the product should be improved or maintained for each of these categories: " + str(categories) + "and return the output in a python dictionary"
  print("prompt": prompt)
  model = "text-davinci-003"
  result = generate_text(prompt, model)
  try:
      index = result.index("{") #just in case the result: output = {}
      result = result[index:].strip() #remove output = 
    
  except:
      pass
  return result


