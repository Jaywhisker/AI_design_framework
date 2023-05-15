#####################################################################################################
# These are functions that are used in the Alt.py file
######################################################################################################
from google.colab import drive
from transformers import pipeline
import pandas as pd
import io
from datetime import datetime

# Main function, first filter, which creates the first filter and passes it through the df_labeller


def filtered_twice(list_of_df, specific_column, search_terms, competitors, keywords):
    # A set list of filter keywords
    first_filter_keywords = [
        'first',
        'game',
        'app',
        'Thanks',
        'great video',
        'video quality',
        'links href a',
        'video review',
        'subscribed',
        'offtopic',
    ]

    second_filter_keywords = [
        'generic',
        'popularity',
        'links',
        'offtopic',
        'suggestion',
        'advice'
    ]

    first_filter = get_first_filter(search_terms[0], competitors, first_filter_keywords)
    filtered_dataframe = []
    for df in list_of_df:
        filtered_dataframe.append(df_labeller_local(df, specific_column, first_filter))
    final = combine_csvs_local(filtered_dataframe,search_terms[0])
    second_filter = get_categorization_filter(keywords, second_filter_keywords)
    df_second_filtered = df_labeller_local(final, specific_column, second_filter)
    return df_second_filtered


# Function that is used to classify each comment in a dataframe into categories
# Requries a database, the column where the comment is and a list of the categories called factors
def df_labeller_local(df, comment_column, factors):
    df_input = df[[comment_column]]
    columns = df_input.columns
    if 'label' not in columns:
        df_input['label'] = 'Not Done'
        df_input['score'] = 'Not Done'
    index = (df_input[df_input.label == "Not Done"].index[0])
    ending_index = df_input.shape[0]
    count = 0
    while index < ending_index:
        try:
            sentence = df_input.loc[index][-3]
            result = classifier(sentence, factors)
            label = result['labels'][0]
            score = result['scores'][0]
            df_input.loc[index]['label'] = label
            df_input.loc[index]['score'] = score
            if score >= 0.3:
                count += 1
                index += 1
        except:
            df_input.loc[index]['label'] = 'Not Valid Sentence'
            df_input.loc[index]['score'] = 'Not Valid Sentence'
            print('skipping' + str(index))
            index += 1
    # Leave here and save one last time to confirm
    # function to save
    return df_input

# Function used to create a list of categories to filter


def get_first_filter(product, competitors, filters):
    filter = []
    filter.append("Comment about " + product)
    for i in competitors:
        filter.append("Comment about " + i)
    filter = filter + filters
    return filter


def get_categorization_filter(keywords, filters):
    final_filter = keywords + filters
    return final_filter


def combine_csvs_local(list_of_df, product):
    product_stuff = pd.DataFrame(columns=['Comments'])
    product_filter = "Comment about " + product
    certainty = 0.3
    for df in list_of_df:
        dataframe = df
        for index, row in dataframe.iterrows():
            comment = str(row['Comments']).strip()
            label = row['label']
            score = row['score']
            if score == "Not Valid Sentence":
                continue
            if score == "Not Done":
                break
            if float(score) > certainty:
                if label == product_filter:
                    product_stuff.loc[len(product_stuff)] = {
                        "Comments": comment}
    return product_stuff


#####################################################################################################
# Below is the collab version of the code that was originally used
######################################################################################################

classifier = pipeline('zero-shot-classification')


def save_to_drive(df, filename):
    path = '/content/drive/My Drive/CSVsForAid/Output/' + filename + '_output.csv'
    with open(path, 'w', encoding='utf-8-sig') as f:
        df.to_csv(f)


def read_from_drive(file_path, specific_column):
    path = '/content/drive/My Drive/CSVsForAid/' + file_path + '.csv'
    df = pd.read_csv(path)
    answer = df[[specific_column]]
    return answer


def check_progress_csv(file_path):
    path = '/content/drive/My Drive/CSVsForAid/Output/' + file_path + '_output.csv'
    try:
        df = pd.read_csv(path)
        return df
    except:
        return 1


def df_labeller_by_20s(filename, factors, specific_column):
    # Label every 20 sets and then save to the csv
    # If df does not exist in proper form first then create
    # Find the column to start

    # Open the csv from drive
    trail = check_progress_csv(filename)
    if isinstance(trail, pd.DataFrame):
        print("Progress csv found, starting from existing index")
        df_input = check_progress_csv(
            filename)[[specific_column, 'label', 'score']]
    else:
        print("No progress csv found, reading from folder")
        df_input = read_from_drive(filename, specific_column)
        # Initialise the dataframe and add the columns if not available
        columns = df_input.columns
        if 'label' not in columns:
            df_input['label'] = 'Not Done'
            df_input['score'] = 'Not Done'

    # iterate through the whole df and every 100, save the information
    # finding the first instance of Not Done
    index = (df_input[df_input.label == "Not Done"].index[0])
    ending_index = df_input.shape[0]
    count = 0

    # Proceed to iterate through
    while index < ending_index:
        if count == 20:
            save_to_drive(df_input, filename)
            count = 0
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            print("saved " + str(index) + " sentence at " + dt_string)

        try:
            sentence = df_input.loc[index][-3]
            result = classifier(sentence, factors)
            label = result['labels'][0]
            score = result['scores'][0]
            df_input.loc[index]['label'] = label
            df_input.loc[index]['score'] = score
            if score >= 0.3:
                count += 1
                index += 1
        except:
            df_input.loc[index]['label'] = 'Not Valid Sentence'
            df_input.loc[index]['score'] = 'Not Valid Sentence'
            print('skipping' + str(index))
            index += 1
    # Leave here and save one last time to confirm
    # function to save
    save_to_drive(df_input, filename)
    return df_input


def combine_csvs(folder_location, product):
    product_stuff = pd.DataFrame(columns=['Comments'])
    product_filter = "Comment about " + product
    certainty = 0.3
    for filename in os.listdir(folder_location):
        print(filename)
        if filename.endswith('.csv'):
            filepath = os.path.join(folder_location, filename)
            dataframe = read_csv(filepath)
            for index, row in dataframe.iterrows():
                comment = str(row['Comments']).strip()
                label = row['label']
                score = row['score']
                if score == "Not Valid Sentence":
                    continue
                if score == "Not Done":
                    break
                if float(score) > certainty:
                    if label == product_filter:
                        product_stuff.loc[len(product_stuff)] = {
                            "Comments": comment}
    return product_stuff
