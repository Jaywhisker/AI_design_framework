# Solid_scraper

## 1. Dependencies

The Codes uses the following libraries:

`amazon_search_results_scraper` <br>
`beautifulsoup4` <br>
`selenium` <br>
`clean-text` <br>
`langdetect` <br>
`google-api-python-client` <br>
`youtube-transcript-api` <br>
`pandas` <br>
`numpy` <br>

Install the libraries with `pip`:
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

## 2. Helper functions

There were several following helper codes that are used in the project.


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

