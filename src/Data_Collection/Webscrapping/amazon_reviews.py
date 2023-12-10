#####################################################################################################
# This is the functions to retrieve the ratings and reviews from Amazon products
# imports: requests, selenium, beautifulsoup, langdetect, cleantext, pandas and helper functions from Helper.

######################################################################################################
# NOTE: This code is purely for EDUCATIONAL purposes as webscrapping Amazon is against its policy. 
# For corporate use, please contact Amazon for its API service.
######################################################################################################


import pandas as pd
import requests
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import itertools
from langdetect import detect
from cleantext import clean
import time
from ...Helper import *

#function to collect all the amazon reviews
#requires: search terms, number of links to look through
#default number of links is all the links
def get_amazon_reviews(search_terms, num_of_links=None, create_csv=True):
    all_links = amazon_search(search_terms)
    if num_of_links == None:  #if default is chosen, update num_of_links to length of all links
        num_of_links = len(all_links)
        
    cleaned_links = creatingreviewlinks(all_links, num_of_links) #create all the review links
    
    all_reviews = [] #contain to hold all reviews
    
    print(cleaned_links)
    print(len(cleaned_links), num_of_links)

    for idx in range(num_of_links): 
        links = cleaned_links[idx][-1] #get review link
        title = cleaned_links[idx][0] #get product title

        #get total reviews for the specific link
        links_reviews = getting_comments_per_link(links)
        review_list = list(zip(itertools.repeat(title), links_reviews)) #format: title, review

        #merge the reviews with other product links reviews
        all_reviews.extend(review_list)

    df = pd.DataFrame(columns=['title', 'links', 'ratings', 'comments'])

    #append all the reviews into a dataframe
    for data in all_reviews:
        df = df.append({'title': data[0], 'links': data[1][0], 'ratings': data[1][1], 'comments': data[1][2]}, ignore_index=True)
    
    if create_csv:
        save_data(df, "amazon reviews", search_terms)
    return df

#function to search for product on amazon using selenium
def amazon_search(search_terms):
    base_url = "https://www.amazon.com/"

    #initialising chrome and going to the url
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(base_url)

    #finding search bar and inputing search_terms to search for products
    search = driver.find_element("xpath", "//*[@id='twotabsearchtextbox']")
    print("The input Element is: ", search)
    search.send_keys(" ".join(search_terms))
    search.send_keys(Keys.RETURN)

    #pausing to let the page load and scrape the page html to store it as amazonpage
    time.sleep(10)
    amazonpage = driver.page_source

    #close the driver
    time.sleep(2)
    driver.close()

    #parse the page 
    soup = BeautifulSoup(amazonpage, "html.parser")
    search_results = soup.find_all('a', {'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'} , href=True)

    search_data = []
    
    for i in search_results:
        try:
            amazon_link = "https://www.amazon.com" + i['href'] #getting full amazon link
            insearch = insearch_result(search_terms, i.text) #check if product on amazon is what we are looking for 
            if insearch == True and "slredirect" not in amazon_link: #if the link is a slredirect, ignore the link as it will affect the url for the next function
                search_data.append([i.text, amazon_link]) #append to list of links to product

        except:
            pass

    return search_data

    

#function to convert product links to the review page for the product
#require: data: list of links, num: number of links we are looking at, can be len(data) to look through all the links or an int to look at top int links
def creatingreviewlinks(data, num): 
    link_list = []

    for idx in range(num):  #to determin number of links we are looking at
        links = data[idx][-1] 
        edited_link = links.replace("dp", "product-reviews") 
        ref_index = edited_link.index("ref")
        review_link = edited_link[:ref_index] + "ref=cm_cr_arp_d_paging_btm_next_6?ie=UTF8&reviewerType=all_reviews&pageNumber="
        link_list.append([data[idx][0], review_link]) #title, new link
        #note: the review_link is missing the int after pageNumber= this is done intentionally as we need to parse through it page afterwards
    return link_list



#function to scrape the amazon reviews for each link
#require a single link
def getting_comments_per_link(link):

    #headers are used such that when the HTTPs:// require is made, some of the meta data is added to make it seem like a real website
    #this is used to bypass Amazon webscrapping check
    #however, the headers may fail after a while and need to be changed
    #alternatively, go to each link with selenium webdriver and get the page source (longer and more tedious process)
    headers = {
        'Host': 'www.amazon.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Referer': 'https://www.google.com/',
        'Cache-Control': 'max-age=0',
        'TE': 'Trailers'
    }

    #setting up defining variable
    total_reviews = [] #container to hold all the reviews
    page_reviews = ["placeholder"] #temporary placeholder for first link
    page_ratings = [] #container to hold all the ratings
    page_num = 1

    while page_reviews != []: #iterates through every page of the review, once it reaches a page with no review, page_review = [] to break while loop
        page_reviews = []
        page_ratings = []

        review_link = link + str(page_num) #change page number in url to loaf next page of comments
        print(review_link)

        response = requests.get(review_link, headers=headers) #access webpage
        soup = BeautifulSoup(response.content, "html.parser") #scrape webpage html with BeautifulSoup
        soup = soup.find('div', {'id': "cm_cr-review_list"}) #specifically review section

        for span_r in soup.find_all("span", "a-size-base review-text review-text-content"): #actual text review
            text = span_r.text.strip() #get the text and strip the trailing whitespace
            text.replace("The media could not be loaded.\n\n\n\n\n", " ") #for reviews with images/videos, the html will return this, remove 
            text = clean(text, no_emoji=True) #remove any emojis from review
            page_reviews.append(text)

        for span in soup.find_all("span", "a-icon-alt"): #reviews /5 stars
            if len(page_ratings) < len(page_reviews): #there are additional reviews at the bottom for other products, once reaches these additional reviews, stop
                page_ratings.append(span.text)

        print(len(page_ratings), len(page_reviews))

        for idx in range(len(page_reviews)): 
            text = page_reviews[idx]
            if text != '':
                language = detect(text) #check the language of the reviews, as Amazon is a global platform, there are reviews in non english languages

                #for simplicity sake, if the review is english, we will use it, else we will ignore
                if language == "en":
                    total_reviews.append([review_link, page_ratings[idx], page_reviews[idx]]) 

        page_num += 1 #move to next page
    
    return total_reviews



