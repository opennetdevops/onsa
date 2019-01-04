#!/usr/bin/python3
import os
from controllers import *
from settings import *

if __name__ == '__main__':
	app.secret_key = os.getenv('SECRET_KEY')
	app.debug = os.getenv('DEBUG')
	app.run(host = os.getenv('HOST'), port = os.getenv('PORT'))
