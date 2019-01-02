from flask import Flask
from mongoengine import connect

import os

app = Flask(__name__)

connect(os.getenv('DB'), host=os.getenv('DB_HOST'), port=int(os.getenv('DB_PORT')))