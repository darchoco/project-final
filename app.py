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

# Set up Post method for handling data inputted into text box
@app.route('/', methods=['POST'])
def my_form_post():
    text = request.form['text']
    processed_text = text.lower()
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

    # Predict the values between the 5 categories: Christian, Country, Hip Hop/Rap, Rhythm and Blues, and Rock
    return_value = model.predict([stats])

    # Define barchart by results

    if return_value == "Christian":
        barchart = "christian_barchart" 
        piechart = "wordcountchristian"

    elif return_value == "Country":
        barchart = "christian_barchart" 
        piechart = "wordcountcountry"

    elif return_value == "Hip Hop/Rap":
        barchart = "rap_barchart" 
        piechart = "wordcounthiphop"

    elif return_value == "Country":
        barchart = "rnb_barchart" 
        piechart = "wordcountrnb"

    elif return_value == "Rock":
        barchart = "rock_barchart" 
        piechart = "wordcountrock"

    else:
        pass


    # Return the predicted genre that will then be inputted on the html
    return render_template('index.html', final_returns = return_value[0], barchart = barchart, piechart = piechart)

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

@app.route("/about")
def about():
    #call html template
    return render_template('about.html')       

if __name__ == '__main__':
    app.run(debug=True)