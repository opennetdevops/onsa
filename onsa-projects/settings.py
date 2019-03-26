from flask import Flask
from mongoengine import connect

import os

app = Flask(__name__)

connect(os.getenv('MONGO_DB'), host=os.getenv('MONGO_DB_HOST'), port=int(os.getenv('MONGO_DB_PORT')))