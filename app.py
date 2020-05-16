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
import joblib
model =joblib.load('genre_guesser.sav')
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
    wordcount = words.wordcount()
    nostopwordcount = words.nostopwordcount()
    positivewordcount = words.positivewordcount()
    positivepercent = round(positivewordcount/nostopwordcount*100,2)
    negativewordcount = words.negativewordcount()
    negativepercent = round(negativewordcount/nostopwordcount*100,2)   
    neutralwordcount = words.negativewordcount()
    neutralpercent = round(neutralwordcount/nostopwordcount*100,2)
    stats = [wordcount,nostopwordcount,positivewordcount,positivepercent,negativewordcount,negativepercent,neutralwordcount,neutralpercent]
    return_value = model.predict([stats])
    print(return_value[0])
    # 0 return is Christian, 1 is Country, 2 is Hip Hop/Rap, 3 is Rhythm and Blues, 4 is rock
    return render_template('index.html', final_returns = return_value[0])

@app.route("/Christian")
def christian():
    #call html template
    return render_template('christian.html')

@app.route("/Country")
def country():
    #call html template
    return render_template('country.html')

@app.route("/hiphop")
def hiphop():
    #call html template
    return render_template('hiphop.html')

@app.route("/rnb")
def rnb():
    #call html template
    return render_template('rnb.html')

@app.route("/rock")
def rock():
    #call html template
    return render_template('rock.html')    

if __name__ == '__main__':
    app.run(debug=True)