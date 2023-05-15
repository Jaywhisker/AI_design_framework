#####################################################################################################
# This is the functions to retrieve the keywords that google shopping has classified the comments for a product into.
# imports:beautifulSoup, selenium, time, pandas and helper functions from Helper.
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import pandas as pd
from ...Helper import *

# Main packaged function
# Outputs: Returns a csv with the title that the keyword came from, number of reviews, the keyword, and the percentage that are either positive or negative comments
#        : The function also returns a dictionary of the keywords after any repetitions have been removed.
# requires: search_terms (list)


def get_googleshopping_reviews(search_terms, create_csv=True):
    product_ids = googleshopping_search(search_terms)
    google_data, google_data_dictionary = googleshopping_keywords(
        product_ids, search_terms)
    # saving data
    if create_csv:
        save_data(google_data, "google shopping", search_terms)
    return google_data_dictionary


# function to search on google shopping using selenium (very similar to shopee)
# requires: insearch_result() function, search terms
def googleshopping_search(search_terms):
    base_url = "https://shopping.google.com/"

    # initialising chrome and going to the url
    driver = webdriver.Chrome("chromedriver.exe")
    driver.get(base_url)

    # finding search bar and searching for search_terms
    search = driver.find_element("xpath", "//*[@id='REsRA']")
    print("The input Element is: ", search)
    search.send_keys(" ".join(search_terms))
    search.send_keys(Keys.RETURN)

    # pausing to let the page load and scrape the page html
    time.sleep(5)
    page = driver.page_source

    # close the driver
    time.sleep(2)
    driver.close()

    # parse the page with beautiful soup
    soup = BeautifulSoup(page, "html.parser")
    product_id = []  # container to hold all the product id

    # get every link in the search result
    for links in soup.find_all('a', href=True):
        # some of the links are advertisments, ignore if they are not google shopping products
        if "/shopping/product" in links['href']:
            # get product id
            end_index = links['href'].index("?")
            id = links['href'][18:end_index]

            # ensure product id is unique as google shopping has multiple listing to the same product
            if id not in product_id:
                product_id.append(id)

    return product_id


# function to obtain the summarised keywords in google_shopping
# requires: list of google shopping product id
def googleshopping_keywords(productID, search_terms):

    # creating the storing varirables
    df = pd.DataFrame(columns=["Title", "Number of Reviews",
                      "Keywords", "Percentage", "Positive/Negative"])
    keyword_dict = {}
    reviewcatchingbin = []

    # base_url
    base_url = "https://www.google.com/shopping/product/"

    for i in range(len(productID)):
        # when there is /offers, it affects getting to the product so we have to cut the /offers in productID
        if "/offers" in productID[i]:
            index = productID[i].index("/offers")
            productID[i] = productID[i][:index]

        # getting product review links
        url = base_url + productID[i] + "/reviews"
        print(url)

        # using selenium to open the website due to same reason as shopee
        driver = webdriver.Chrome("chromedriver.exe")
        driver.get(url)

        # let page load before taking the html source code
        time.sleep(5)
        page = driver.page_source
        time.sleep(2)

        # close the driver
        driver.close()

        # parse the page to get the title, anyreviews, numreviews
        soup = BeautifulSoup(page, 'html.parser')
        title = soup.find("div", {"class": "f0t7kf"}).text
        anyreviews = soup.find("div", {"class": "rktlcd"})
        numreviews = soup.find("span", "HiT7Id").text
        print(numreviews)

        # if there are no reviews for the product, anyreviews will return None
        if anyreviews == None:
            print("No reviews found")
            pass

        # some product have different ID but look at the same reviews (this is due to different products that have different listing for different colours)
        # to prevent repeated data, ignore the reviews
        elif numreviews in reviewcatchingbin:
            print("repeated review")
            pass

        else:
            # checking if the product name is accurate
            intitle = insearch_result(search_terms, title)
            # add the number of reviews into review catching bin
            reviewcatchingbin.append(numreviews)

            if intitle:
                for span in soup.find_all("span", "QIrs8"):
                    text = span.text
                    if text == "Select to view all reviews":  # ignore first text in this span
                        pass

                    # data will be in the format of: View xx reviews about 'keyword'. xx% of the reviews are 'positive/negative'.
                    else:
                        reviews_index = text.index("r")
                        about_index = text.index("about")
                        full_stop_index = text.index(".")
                        percentage_index = text.index("%")

                        # slicing View xx r -> xx
                        num_of_reviews = text[4: reviews_index].strip()
                        # slicing about 'keyword'. -> keyword
                        keywords = text[about_index +
                                        len("about")+1: full_stop_index]
                        percentage = text[full_stop_index +
                                          2: percentage_index]  # . xx% -> xx
                        positivenegative = text[-9:-1]  # positive / negative

                        keyword_dict[keywords] = positivenegative
                        df = df.append({"Title": title, "Number of Reviews": num_of_reviews, "Keywords": keywords,
                                       "Percentage": percentage, "Positive/Negative": positivenegative}, ignore_index=True)
    print(df)

    # returning dictionary because total_uncleaned_keywords() requires dictionary
    return df, keyword_dict
