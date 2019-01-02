from flask import render_template

from settings import *
from models import *

@app.route('/helloworld', methods=['GET'])
def hello_world():
    return render_template('helloworld.html')