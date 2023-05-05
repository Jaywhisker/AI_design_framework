# Solid_scraper

Insert intro paragraph

## Dependencies

Install the following libraries with `pip`:
```
pip install amazon_search_results_scraper
pip install beautifulsoup4
pip install selenium
pip install clean-text
pip install langdetect
pip install google-api-python-client
pip install youtube-transcript-api
pip install pandas
pip install numpy
```

## Helper.py (helper functions)

There were several following helper codes that are used in the project.

-----

`insearch_result`: A function used to check if the title of the product contains all the words of the main search term. <br>
For example, if the search term is `['dyson', 'am07']`, all titles that will get choosen must have these 2 words in their titles.
```
def insearch_result(search_term, title):
    title = title.lower() #as search_term is in lower case
    for keywords in search_term:
        if keywords not in title:
            print(title)
            return False
    return True
```

-----
`save_data`: A function used to save dataframes into csvs inside a folder under Data and followed by a combination of the search_terms
```
import os
import csv

def save_data(data, file_name, search_terms):
    try: # Create directory named after search terms
        os.makedirs("Data/%s" % " ".join(search_terms)) 
        print("Directory created")

    except FileExistsError:
        print("Directory exists")

    #save to csv file
    data.to_csv("Data/%s/%s.csv" %(" ".join(search_terms), file_name))
```
-----


## Scraper.py (Web scraping functions)
This file is a collection of scrapper functions used to collect data from various websites. <br>
Current functions: <br>
`Amazon`: 

`Shopee`: 

`get_youtube_captions`: A function that takes the search_terms, an api_key from ____________ and the count of number of videos to be scanned and returns a csv with all the captions of the respective youtube videos.

`get_youtube_comments`:  A function that takes the search_terms, an api_key from ____________ and the count of number of videos to be scanned and returns a csv with the comments from those videos. 

`get_googleshopping_reviews`: A function that takes the search_terms and returns a csv of the keywords collected as well as a dictionary of keywords.

`get_reddit_comments`: A function that takes the search_terms, an api_key from reddit apps and the count of the number of posts to be scanned and returns a csv with the comments from those threads.

