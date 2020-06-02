import numpy as np
import requests
import pandas as pd
import pprint as pp
import numpy as np
import sqlalchemy
import matplotlib.pyplot as plt
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
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


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
    # Pull data from submitted lyrics
    text = request.form['text']
    if len(text)==0:
       return render_template('index.html', final_returns= "No Lyrics Inputted")
    # Convert all words to lowercase to allow for similar identification
    processed_text = text.lower()

    # Initiate class with processed_text to start tokenizing data
    words = worddata.word_calcs(processed_text)
    wordcount = words.wordcount()
    nostopwordcount = words.nostopwordcount()
    positivewordcount = words.positivewordcount()
    positivepercent = round(positivewordcount/nostopwordcount*100,2)
    negativewordcount = words.negativewordcount()
    negativepercent = round(negativewordcount/nostopwordcount*100,2)   
    neutralwordcount = words.neutralwordcount()
    neutralpercent = round(neutralwordcount/nostopwordcount*100,2)
    stats = [wordcount,nostopwordcount,positivewordcount,positivepercent,negativewordcount,negativepercent,neutralwordcount,neutralpercent]

    # Define values needed for pie chart of passed lyrics, create pie chart in same style as static pie charts for genre data
    sizes = [positivepercent,negativepercent,neutralpercent]
    labels = 'positive','negative','neutral'
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes,labels=labels, autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    ax1.set(title='Count of Word Types for Inputted Lyrics')
    plt.savefig('static/currentpie.png', dpi = 100)
    plt.close()

    # Get list of words for count
    nostopwordlist = words.nostopwordlist()
    wordfreq = []
    for word in nostopwordlist:
        wordfreq.append(nostopwordlist.count(word))
    word_df = pd.DataFrame(nostopwordlist, columns = ["Word"])
    word_df["Frequency"] = wordfreq
    word_df = word_df[word_df.Word !='\'' ]
    word_df = word_df[word_df.Word !='\'s' ]
    word_df = word_df[word_df.Word !='n\'t' ]
    word_df = word_df[word_df.Word !='\'m' ]
    word_df = word_df[word_df.Word !='\'ve' ]
    word_df = word_df[word_df.Word !='\'ll' ]
    word_df = word_df[word_df.Word !='\'re' ]
    word_df = word_df[word_df.Word !=',' ]
    word_df = word_df.drop_duplicates().sort_values(by='Frequency', ascending=False).head(10)
    x_axis = np.arange(0,len(word_df["Word"].tolist()))
    tick_locations = []
    for x in x_axis:
        tick_locations.append(x)
    
    frequency = word_df["Frequency"].tolist()
    plt.title("Most Common Words from Inputted Lyrics")
    plt.xlabel("Words")
    plt.ylabel("Frequency")
    plt.xlim(-0.75, len(word_df["Word"].tolist())-.25)
    plt.ylim(0, max(frequency) + .5)

    plt.bar(x_axis, frequency, facecolor="red", alpha=0.75, align="center")
    plt.xticks(tick_locations, word_df["Word"].tolist())
    plt.savefig('static/currentbar.png', dpi =100) 
    plt.close()

    
        
    # Predict the values between the 5 categories: Christian, Country, Hip Hop/Rap, Rhythm and Blues, and Rock
    return_value = model.predict([stats])

    # Define barchart by results

    if return_value == "Christian":
        barchart = "christian_barchart" 
        piechart = "wordcountchristian"

    elif return_value == "Country":
        barchart = "country_barchart" 
        piechart = "wordcountcountry"

    elif return_value == "Hip Hop/Rap":
        barchart = "rap_barchart" 
        piechart = "wordcounthiphop"

    elif return_value == "Country":
        barchart = "country_barchart" 
        piechart = "wordcountcountry"

    elif return_value == "Rock":
        barchart = "rock_barchart" 
        piechart = "wordcountrock"

    elif return_value == "Rhythm and Blues":
        barchart = "rnb_barchart" 
        piechart = "wordcountrnb"
    else:
        barchart = None
        piechart = None
        


    # Return the predicted genre that will then be inputted on the html
    return render_template('index.html', final_returns = return_value[0], barchart = barchart, piechart = piechart, currentpie = "currentpie", currentbar = "currentbar")

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

# No caching at all for API endpoints.
@app.after_request
def add_header(response):
    # response.cache_control.no_store = True
    if 'Cache-Control' not in response.headers:
        response.headers['Cache-Control'] = 'no-store'
    return response
if __name__ == '__main__':
    app.run(debug=True)