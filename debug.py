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

text = '''Risin' up, back on the street Did my time, took my chances Went the distance, now I'm back on my feet Just a man and his will to survive So many times, it happens too fast You trade your passion for glory Don't lose your grip on the dreams of the past You must fight just to keep them alive It's the eye of the tiger, it's the thrill of the fight Risin' up to the challenge of our rival And the last known survivor stalks his prey in the night And he's watchin' us all with the eye of the tiger Face to face, out in the heat Hangin' tough, stayin' hungry They stack the odds 'til we take to the street For the kill with the skill to survive It's the eye of the tiger, it's the thrill of the fight Risin' up to the challenge of our rival And the last known survivor stalks his prey in the night And he's watchin' us all with the eye of the tiger Risin' up, straight to the top Had the guts, got the glory Went the distance, now I'm not gonna stop Just a man and his will to survive It's the eye of the tiger, it's the thrill '''
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
ax1.set(title='count of word types')
plt.savefig('currentpie.png')
plt.close()

# Get list of words for count
nostopwordlist = words.nostopwordlist()
wordfreq = []
for word in nostopwordlist:
    wordfreq.append(nostopwordlist.count(word))
word_df = pd.DataFrame(nostopwordlist, columns = ["Word"])
word_df["Frequency"] = wordfreq
word_df = word_df.drop_duplicates().sort_values(by='Frequency', ascending=False).head(10)
x_axis = np.arange(0,len(word_df["Word"].tolist()))
tick_locations = []
for x in x_axis:
    tick_locations.append(x)

frequency = word_df["Frequency"].tolist()
plt.title("Most Common Words from inputted lyrics")
plt.xlabel("Words")
plt.ylabel("Frequency")
plt.xlim(-0.75, len(word_df["Word"].tolist())-.25)
plt.ylim(0, max(frequency) + .5)

plt.bar(x_axis, frequency, facecolor="red", alpha=0.75, align="center")
plt.xticks(tick_locations, word_df["Word"].tolist())
plt.savefig('currentbar.png') 


