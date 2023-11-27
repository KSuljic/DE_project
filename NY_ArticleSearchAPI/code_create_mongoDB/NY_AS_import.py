#Initial imports
import requests
import json
import pymongo
from pymongo import ReplaceOne

import time
import random
import numpy as np


def natural_variation_delay(min_delay=20, max_delay=30):
    """
    Waits for a random amount of time between `min_delay` and `max_delay` seconds.
    """
    t_wait = random.uniform(min_delay, max_delay)
    print(t_wait)
    time.sleep(t_wait)



# Access API
API_KEY = 'PAKnickrXf68F5WPgbBgEe2Ine6vI7oi'
url = 'https://api.nytimes.com/svc/search/v2/'
endpoint = 'articlesearch.json'



# Access DB
from pymongo import MongoClient
# Create a connection to the MongoDB server
client = MongoClient('localhost', 27017)
# Access the database
db = client['NY_ArticleSearch']
collection = db['ny_articles']


##

DOCS = []

# Get the maximum _id value from the collection
max_id = collection.find_one(sort=[("_id", -1)])
index_counter = max_id['_id'] + 1 if max_id else 0

# Main loop
page = 50
attempts = 0

while page < 100:
    #while attempts < 5:
    try:
        print(f"Trying page {page}, attempt {attempts + 1}")

        res = requests.get(f'{url}/{endpoint}?page={page}&api-key={API_KEY}')
        res.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code

        articles_names_json = res.json()
        documents = articles_names_json.get('response')['docs']

        # Assign a new _id to each document
        for doc in documents:
            doc['_id'] = index_counter
            index_counter += 1

        DOCS.extend(documents)

        natural_variation_delay()

        page += 1

        #break

    except TypeError:
            # TypeError handling here
        print(f"TypeError occurred on page {page}, attempt {attempts + 1}")
        attempts += 1
        natural_variation_delay()  # Wait before retrying
        natural_variation_delay()

    # except requests.HTTPError as http_err:
    #     # Handle HTTP errors here
    #     print(f"HTTPError occurred: {http_err}")
    #     break  # Exit the attempts loop and go to the next page


    # except requests.RequestException as req_err:
    #     # Handle other requests exceptions here
    #     print(f"RequestException occurred: {req_err}")
    #     break  # Exit the attempts loop and go to the next page





try:
    collection.insert_many(DOCS, ordered=False)
except pymongo.errors.BulkWriteError as bwe:
    print(bwe.details)