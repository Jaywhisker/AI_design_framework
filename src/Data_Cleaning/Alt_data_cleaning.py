#####################################################################################################
# These are functions that are used in the Alt.py file
# It should be noted that the siamese_analysis function was run on collab and has not been tested locally
######################################################################################################
from scipy import spatial
import gensim.downloader as api
import numpy as np

# This is the main function that is called in the Alt.py file
# It is prepared to handle the 3 variables received, regardless if they are list or dictionary


def keyword_cleaner(strengths, flaws, google_keywords):
    if type(strengths) == list:
        op1 = strengths
    else:
        op1 = strengths.keys()
    if type(flaws) == list:
        op2 = flaws
    else:
        op2 = flaws.keys()
    if type(google_keywords) == list:
        op3 = google_keywords
    else:
        op3 = google_keywords.keys()
    main_list = combine_keywords(op1, op2, op3)
    main_list = siamese_analysis(main_list)
    main_list = create_keywords(main_list)
    return main_list


# A function that takes in 3 list and combines them into a list of keywords (removing any exact repetitions)
def combine_keywords(strengths: list, flaws: list, google_keywords: list):
    keywords = []
    for strength in strengths:
        if strength not in keywords:
            keywords.append(strength).lower()
    for flaw in flaws:
        if flaw not in keywords:
            keywords.append(flaw).lower()
    for goolge in google_keywords:
        if goolge not in keywords:
            keywords.append(goolge).lower()
    return keywords


# A function that performs siamese_analysis on the lists of words and removes any words that are too similar according to the model
# Go to Collab
def siamese_analysis(All_keywords):
    # choose from multiple models https://github.com/RaRe-Technologies/gensim-data
    model = api.load("glove-wiki-gigaword-50")

    keywords = All_keywords

    def preprocess(s):
        return [i.lower() for i in s.split()]

    def get_vector(s):
        return np.sum(np.array([model[i] for i in preprocess(s)]), axis=0)

    vector_data = []
    for keyword in keywords:
        print(keyword)

        value = get_vector(keyword)
        vector_data.append(value)

    cleaned_keywords = []

    for i in range(len(vector_data)):
        for j in range(i, len(vector_data)):
            similarity = 1 - \
                spatial.distance.cosine(vector_data[i], vector_data[j])
            if similarity < 0.2:
                cleaned_keywords.append(keywords[i])
                cleaned_keywords.append(keywords[j])
                # print(keywords[i], keywords[j])

    cleaned_keywords = list(set(cleaned_keywords))
    return cleaned_keywords

# A function that takes a list and remove any strings which are substrings of larger strings


def create_keywords(cleaned_keywords):
    cleaned_keywords.sort(key=len, reverse=False)

    for i in range(len(cleaned_keywords)):
        cleaned_keywords[i] = cleaned_keywords[i].lower()
    print(cleaned_keywords)

    # loop through each string in the list
    for i in range(len(cleaned_keywords)):
        # compare the string with all subsequent strings in the list
        for j in range(i+1, len(cleaned_keywords)):
            if cleaned_keywords[i] in cleaned_keywords[j]:
                # if the current string is a substring of another string, remove it from the list
                cleaned_keywords.pop(i)
                break
        else:
            # if the current string is not a substring of any subsequent strings, move on to the next string
            continue
        # if the current string was removed from the list, adjust the index accordingly
        i -= 1
    return cleaned_keywords
