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
-----

## Helper.py (helper functions)

This file contains several helper functions that were used in the project.


`insearch_result`: A function used to check if the title of the product contains all the words of the main search term. <br>
For example, if the search term is `['dyson', 'am07']`, all titles that will get choosen must have these 2 words in their titles.

`save_data`: A function used to save dataframes into csvs inside a folder under Data and followed by a combination of the search_terms

`get_data`: A function used to read csv files and converting them into a nested list
-----
## Scraper folder (Web scraping functions)
This file is a collection of scrapper functions used to collect data from various websites. <br>
In order to use each function in a new python file, place Helper.py and the specific python file in the same directory as your python file and run the code in the codeblock provided.


Current functions: <br>
 
`get_amazon_reviews`: A function that takes the search_terms and the count of number of links to be looked through. The function will return a dataframe with the product title, the link, the ratings and the respective reviews.
```
from amazon_reviews import *
from Helper import *

#Parameters for functions
search_terms = ['pillow', 'case']
Universal_count = None (will automatically checks all links)

#data = get_amazon_reviews(search_terms, None)
#file_name = "YOUR DIRECTORY HERE"
#save_data(data, file_name, search_terms)
```

`get_all_shopee_reviews`: A function that takes the search_terms and the count of number of links to be looked through. The function will return a dataframe with the link, the ratings and the respective reviews.
```
from shopee_reviews import *
from Helper import *

#Parameters for functions
search_terms = ['pillow', 'case']
Universal_count = None (will automatically check all links)

#data = get_all_shopee_reviews(search_terms, None)
#file_name = "YOUR DIRECTORY HERE"
#save_data(data, file_name, search_terms)
```

`get_youtube_captions`: A function that takes the search_terms, an api_key from ____________ and the count of number of videos to be scanned and returns a dataframe with all the captions of the respective youtube videos.
```
from youtube_captions import *
from Helper import *

# Parameters for functions
search_terms = ['pillow', 'case']
youtube_api_key = INSERT_YOUR_KEY_HERE
Universal_count = 5

#data = get_youtube_captions(search_terms, youtube_api_key, Universal_count)
#file_name = "YOUR DIRECTORY HERE"
#save_data(data, file_name, search_terms)
```
`get_youtube_comments`:  A function that takes the search_terms, an api_key from ____________ and the count of number of videos to be scanned and returns a dataframe with the comments from those videos. 
```
from youtube_comments import *
from Helper import *

# Parameters for functions
search_terms = ['pillow', 'case']
youtube_api_key = INSERT_YOUR_KEY_HERE
Universal_count = 5

#data = get_youtube_comments(search_terms, youtube_api_key, Universal_count)
#file_name = "YOUR DIRECTORY HERE"
#save_data(data, file_name, search_terms)
```

`get_googleshopping_reviews`: A function that takes the search_terms and returns a dataframe of the keywords collected as well as a dictionary of keywords.
```
from google_shopping import *
from Helper import *

# Parameters for functions
search_terms = ['pillow', 'case']

#data = get_googleshopping_reviews(search_terms)
#file_name = "YOUR DIRECTORY HERE"
#save_data(data, file_name, search_terms)
```

`get_reddit_comments`: A function that takes the search_terms, an api_key from reddit apps and the count of the number of posts to be scanned and returns a dataframe with the comments from those threads.
```
from reddit_comments import *
from Helper import *

# Parameters for functions
search_terms = ['pillow', 'case']
number_of_posts = 5
reddit_api_key = INSERT_YOUR_KEY_HERE
reddit_secret =INSERT_YOUR_KEY_HERE

#data = get_reddit_comments(search_terms, number_of_posts, reddit_api_key, reddit_secret)
#file_name = "YOUR DIRECTORY HERE"
#save_data(data, file_name, search_terms)
```

`get_apple_insider_comments`: A function that takes a list of articles and return a dataframe with the comments from the links provided.
```
from apple_insider import *
from Helper import *

# Parameters for functions
list_of_articles = [INSERT_YOUR_ARTICLES_HERE]

#data = get_apple_insider_comments(list_of_articles)
#file_name = "YOUR DIRECTORY HERE"
#save_data(data, file_name, search_terms)
```

`get_hardware_zone_comments`: A function that takes the number of pages to scan from the iphone chat room on the hardware zone and returns a dataframe with the comments from the various pages scanned.

```
from Hardwear_zone import *
from Helper import *

# Parameters for functions
Universal_count = 5

#data = get_hardware_zone_comments(Universal_count)
#file_name = "YOUR DIRECTORY HERE"
#save_data(data, file_name, search_terms)
```
