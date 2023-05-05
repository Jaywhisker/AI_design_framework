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

def insearch_result(search_term, title):
    title = title.lower() #as search_term is in lower case
    for keywords in search_term:
        if keywords not in title:
            print(title)
            return False
    return True
  
  
