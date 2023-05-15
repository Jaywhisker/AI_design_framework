#####################################################################################################
# This is the functions to retrieve the reviews, ratings from shopee products
# imports: requests, selenium, beautifulsoup, pandas, time and helper functions from Helper.

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from cleantext import clean
from ...Helper import *

#collecting all the shopee reviews
#requires: search_terms, number of links to look through
#default number of links will be all available links
def get_all_shopee_reviews(search_terms, num_links=None, create_csv=True):
  all_links = shopee_search(search_terms) #getting all the links
  if num_links == None: #if default number of links is chosen
        num_links = len(all_links) #update number of links to be all the links
        
  data = pd.DataFrame(columns=["url", "ratings", "reviews"])
  
  #iterate through all the links
  for i in range(num_links):
      links = all_links[i]
      result = shopee_reviews_per_link(links)
    
      if result == []: #if no reviews, ignore
          pass
      else:
          for i in range(len(result)): #if have review, append the reviews and ratings to the dataframe
              data = data.append({"url": links, "ratings": result[i][0], "reviews": result[i][1]}, ignore_index = True)
  if create_csv:
    save_data(data, "shopee reviews", search_terms)
  return data


#function to search for product on shopee
#using selenium in this scenario (selenium is an automated web driver)
def shopee_search(search_terms):
    base_url = "https://shopee.sg/"

    #initialising chrome and going to the url
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(base_url)

    #finding search bar and inputing search_terms to search for products
    search = driver.find_element("xpath", "//*[@id='main']/div/header/div[2]/div/div[1]/div[1]/div/form/input")
    print("The input Element is: ", search)
    search.send_keys(" ".join(search_terms))
    search.send_keys(Keys.RETURN)

    #pausing to let the page load and scrape the page html to store it as shopeepage
    time.sleep(10)
    shopeepage = driver.page_source

    #close the driver
    time.sleep(2)
    driver.close()

    #parse the page 
    soup = BeautifulSoup(shopeepage, "html.parser")

    links_list = [] #container for all the links
 
    #iterating through all the links in the first page of search terms
    for data in soup.find("div", {"class": "row shopee-search-item-result__items"}):
        for links in data.find_all("a", href = True): 
            intitle = insearch_result(search_terms, links["href"]) #check if searchterms are in title
            if intitle:
                links_list.append(base_url[:-1] + links["href"]) #add to links container if search terms in title

    return links_list



#function to get all the shopee reviews in a link
def shopee_reviews_per_link(url):

    #container of variables
    total_data  = []
    comments_list = []
    ratings_list = []

    #shopee uses Javascript to dynamically generate content, the base source html doesn't provide the reviews as it requires the javascript to run the script to load the reviews
    #hence we need to use selenium again to initialise chrome and load the html and run the javascript code 
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(url)

    #letting the javascrip in the page load before getting the page html
    time.sleep(10)
    page = driver.page_source
    time.sleep(2)

    #now that the javascript content is generated, parse the html code
    soup = BeautifulSoup(page, 'html.parser')

    #get the ratings of the product
    total_ratings = soup.find_all("div", {"class": "_1k47d8"})

    #if there are no reviews on the product, it will cause an error, if so close the webpage and return [] as the is no reviews
    try:
        total_ratings = total_ratings[-1].text 
    except:
        driver.close()    
        return []

    #if there are ratings, find all the buttons in the html. The last button is always the next_button to get the next page of reviews
    #this is an example of the Javascript section of the html, unlike amazon, the url of the page does not change, 
    #however the review section will dynamically change when the next button is called
    buttons = driver.find_elements(By.TAG_NAME, 'button')
    next_button = buttons[-1]
    
    #as there are 6 pages on every page, total_ratings//6 determines the number of pages of reviews
    for i in range(int(total_ratings)//6 ):
        for reviews in soup.find_all("div", {"class": "shopee-product-rating"}):

          #try statement is called as some reviews are just images with no text which will lead to an error when trying to call .text
            try:
                #getting reviews
                comment = reviews.find("div", {"class": "Rk6V+3"}).text 
                comment = clean(comment, no_emoji = True) #removing emojis
                comments_list.append(comment) #adding to comment contained
                #getting ratings
                #shopee ratings method is done by using images, 4/5 would have 4 solid star image + 1 border start image
                ratings = reviews.find("div", {"class" : "shopee-product-rating__rating"}) 
                image = ratings.find_all("svg", {"class": "shopee-svg-icon icon-rating-solid--active icon-rating-solid"}) #finding number of solid star image
                ratings_list.append(len(image)) 
            
            except:
                pass

        #after looking through all the reviews, click the next button
        driver.execute_script("arguments[0].click();", next_button) 
        
        #let the next page of reviews load and get the updated html source page to reparse by beautiful soup
        #repeat the cycle until end of all reviews
        time.sleep(5)
        page = driver.page_source
        soup = BeautifulSoup(page, 'html.parser')

    #close the webpage and add the data
    driver.close()    
    total_data.extend(list(zip(ratings_list, comments_list)))
    print( len(ratings_list), len(comments_list), len(total_data))

    return total_data



