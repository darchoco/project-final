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
model =joblib.load('genreguesser.sav')
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
    negativewordcount = words.negativewordcount()
    neutralwordcount = words.negativewordcount()
    stats = [wordcount,nostopwordcount,positivewordcount,negativewordcount,neutralwordcount]
    return_value = model.predict([stats])
    # 0 return is Christian, 1 is Country, 2 is Hip Hop/Rap, 3 is Rhythm and Blues, 4 is rock
    
    if return_value[0] ==0:
        final_return = "Christian"
        return final_return
    elif return_value[0]  ==1:
        final_return = "Country"
        return final_return
    elif return_value[0] ==2:
        final_return = "Hip Hop/Rap"
        return final_return
    elif return_value[0] ==3:
        final_return = "Rhythm and Blues"
        return final_return
    elif return_value[0] ==4:
        final_return = "Rock"
        return final_return      
    else:
        return print("STAHP I'M ALREADY DEAD")

if __name__ == '__main__':
    app.run(debug=True)