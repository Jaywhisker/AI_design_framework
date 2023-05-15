#####################################################################################################
# This is the another main code file that will run an alternate framework that was also developed
######################################################################################################

from transformers import pipeline
import io
from datetime import datetime
import string
from transformers import pipeline
import pandas as pd
import os
from scipy import spatial
import gensim.downloader as api
import numpy as np

from Data_Collection.Webscrapping.amazon_reviews import *
from Data_Collection.Webscrapping.reddit_comments import *
from Data_Collection.Webscrapping.youtube_comments import *
from Data_Collection.Webscrapping.hardware_zone import *
from Data_Collection.Design_Opportunities.GPT_keyword import *
from Data_Collection.Design_Opportunities.google_shopping import *
from Data_Cleaning.Alt_data_cleaning import *
from Data_Categorisation.Alt_data_categorisation import *
from Sentiment_Analysis.Alt_sentiment_analysis import *
from Generating_Design_Opportunities.Alt_design_opportunities import *


# Input: search_terms (list)
# Output:
#       3 Categories the product should improve in,
#       Ways the product can be improved in the respective categories,
#       A design problem statement for the product

def Generating_Design_Opportunities_Alt(search_terms, ytapi, reddit_id, reddit_secret, gpt3api, model="text-davinci-003"):
    # ============================================================================================
    #                           FORMING design keywords
    # ============================================================================================
    print("Getting Google Shopping Keywords")
    Google_shopping_dictionary = get_googleshopping_reviews(
        search_terms, False)
    print("Getting design specifications from GPT-3")
    design_flaws = get_flaws(search_terms, model, gpt3api)
    design_strengths = get_strength(search_terms, model, gpt3api)
    print("Combinging keywords")
    All_keywords = keyword_cleaner(
        Google_shopping_dictionary, design_flaws, design_strengths)
    competitors = get_competitors(search_terms, model, gpt3api)
    # ============================================================================================
    #                            DATA COLLECTION webscrapping
    # ============================================================================================
    print("Getting Amazon Reviews")
    amazon_data = get_amazon_reviews(
        search_terms, num_of_links=None, create_csv=False)
    print("Getting Youtube Comments")
    youtube_comments = get_youtube_comments(
        search_terms, ytapi, count=5, create_csv=False)
    print("Getting Reddit Comments")
    reddit_data = get_reddit_comments(
        search_terms, 5, reddit_id, reddit_secret, create_csv=False)
    print("Getting hardware zone data")
    hardware_zone_data = get_hardware_zone_comments(5, create_csv=False)
    # ============================================================================================
    #                                DATA CATEGORISATION
    # ============================================================================================
    print("Putting dataframes into a list")
    data_list = [amazon_data, youtube_comments,
                 reddit_data, hardware_zone_data]
    print("Filter the data using zero shot classification")
    filtered_df = filtered_twice(
        data_list, "comments", search_terms, competitors, All_keywords)
    # ============================================================================================
    #                               SENTIMENT ANALYSIS
    # ============================================================================================
    print("Labelling the data using sentiment analysis")
    tabulated_score, positive_comments, negative_comments = sentiment_labeller(
        filtered_df, All_keywords)
    # ============================================================================================
    #                               GENERATING DESIGN OPPORTUNITIES
    # ============================================================================================
    print("Extracting top 3 categories and corresponding comments")
    top_3_categories, extracted_comments = get_outputs(
        tabulated_score, positive_comments, negative_comments)
    print("Getting best way to improve in the categories")
    best_way_to_improve = get_best_way_to_improve_quality(
        top_3_categories, extracted_comments, search_terms[0])
    print("Creating design prompt")
    design_problem_statement = get_design_problem_statement(
        search_terms[0], top_3_categories)

    print("writing to a txt file")
    with open('output.txt', 'w') as f:
        f.write('This is the output for the product: ')
        f.write(search_terms[0] + '\n\n\n')

        f.write("Output one: Product's weakest areas" + '\n')
        f.write('According to the comments analysed, the product is weakest in the following categories: ' + '\n\n')

        categories_to_improve = ""
        for i in range(len(top_3_categories)):
            categories_to_improve = categories_to_improve + top_3_categories[i]
            if i != len(top_3_categories) - 1:
                categories_to_improve = categories_to_improve + ', '

        f.write(categories_to_improve + '\n\n')

        f.write('\n\n')

        f.write(
            "Output two: Suggested means to improve the product's weakest areas:" + '\n')
        f.write(
            'These are the suggestions for a company to improve in the following categories: ' + '\n\n')
        for j in best_way_to_improve:
            f.write(j + " : " + best_way_to_improve[j] + '\n\n')

        f.write('\n\n')

        f.write("Output three: A design problem statement to start designers ideating on improve the product:" + '\n')
        f.write(design_problem_statement)
