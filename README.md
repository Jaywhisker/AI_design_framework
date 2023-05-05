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

### Calling the functions
In order to use the functions above in a new python file, place the Helper.py and Scraper.py files in the same location and import the function from Scraper.py.

```
from Scraper import *

# Parameters for functions
search_terms = ['pillow', 'case']
youtube_api_key = INSERT_YOUR_KEY_HERE
Universal_count = 5
reddit_api_key = INSERT_YOUR_KEY_HERE
reddit_secret =INSERT_YOUR_KEY_HERE

#How to call each function (uncomment as needed)
#get_youtube_captions(search_terms, youtube_api_key, Universal_count)
#get_youtube_comments(search_terms, youtube_api_key, Universal_count)
#get_googleshopping_reviews(search_terms)
#get_reddit_comments(search_terms, number_of_posts, reddit_id, reddit_secret)
```
