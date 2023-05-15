#####################################################################################################
# These are functions that are used in the Alt.py file
######################################################################################################
from ...Helper import *


def get_outputs(Qualatative, positive, negative):
    points_to_focus_on = Qualatative[:3]
    # points store the quality to focus on
    # extracted comments stores the comments on what has been said about the product
    points = []
    extracted_comments = []
    for x, y in points_to_focus_on:
        points.append(x)
        if y < 0:  # means negative  so get  the negative word bank
            extracted_comments.append(negative[x])
        else:
            extracted_comments.append(positive[x])
    return points, extracted_comments

# This function then takes the points and extracted comments and ask chatgpt to summarise the best way to improve in the various categories


def get_best_way_to_improve_quality(points, extracted_comments, product):
    ways_to_improve = {}
    for i in range(len(points)):
        prompt = "According to the extracted comments, what is the best way for the company of the " + product + \
            " to improve following aspect of the " + product + "? Aspect: " + \
            points[i] + ". Extracted Comments: " + extracted_comments[i]
        response = ask_gpt(prompt)
        print(response)
        ways_to_improve[points[i]] = response
    return ways_to_improve

# This function will take the points and use openai to create a design prompt for the product using the points extracted previously


def get_design_problem_statement(product, points):
    pointers = ""
    for i in points:
        pointers = pointers + i
    prompt = "Create a Design problem statement to improve the " + \
        product + " centering around the following qualities: " + pointers
    return ask_gpt(prompt)
