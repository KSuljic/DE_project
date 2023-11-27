# Access DB
from pymongo import MongoClient
# Create a connection to the MongoDB server
client = MongoClient('localhost', 27017)
# Access the database
db = client['NY_ArticleSearch']
collection = db['articles']

collection.delete_many({})
