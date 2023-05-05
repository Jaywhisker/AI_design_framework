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

```
#function to ensure that the product that we are scrapping reviews from is the actual product as search terms may return irrelevant products
#require: search_term to be a list of words making up the product in lower case
def insearch_result(search_term, title):
    title = title.lower() #as search_term is in lower case
    for keywords in search_term:
        if keywords not in title:
            print(title)
            return False
    return True
```

