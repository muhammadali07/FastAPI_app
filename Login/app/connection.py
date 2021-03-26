from pymongo import MongoClient
# import settings

connection = MongoClient('127.0.0.1', 27017)
db = connection.pulsa