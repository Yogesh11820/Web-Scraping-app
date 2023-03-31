from flask import Flask
from flask_pymongo import PyMongo


app = Flask(__name__)
app.config['MONGO_URI']  = 'mongodb://localhost:27017/todo_db'
mongodb_client = PyMongo(app)
db = mongodb_client.db



from routes import *

if __name__ == '__main__':
    app.run(debug=True)
    