from pymongo import MongoClient
from pymongo.server_api import ServerApi
from pymongo.errors import PyMongoError
from urllib.parse import quote
import os
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo

app = Flask(__name__)
username = 'User_1'
password = os.environ.get('MONGO_PASSWORD')
username_ = quote(username)
password_ = quote(password)
uri = f"mongodb+srv://{username_}:{password_}@cluster0.gubmoqj.mongodb.net/WebScrape?retryWrites=true&w=majority"
app.config["MONGO_URI"] = uri

try:
    mongo = PyMongo(app)
    print("PyMongo instance initialized")
except PyMongoError as e:
    print(e)
    exit()

client = MongoClient(uri, server_api=ServerApi('1'))

try:
    client.admin.command('ping')
    print("Successfully connected to MongoDB")
except Exception as e:
    print(e)

from routes import *



if __name__ == '__main__':
    app.run(debug=True)
