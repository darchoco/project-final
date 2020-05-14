import numpy as np
import requests
import pandas as pd
import pprint as pp
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from Models import worddata
from flask import Flask, jsonify, render_template, request


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    #call html template
    return render_template('index.html')

@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.lower()
    print(processed_text)
    words = worddata.word_calcs(processed_text)
    return str(words.negativewordcount())

if __name__ == '__main__':
    app.run(debug=True)