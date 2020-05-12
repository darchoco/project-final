# Load the dataset and convert it to lowercase :
# textFileName = 'lyricsText.txt'
# raw_text = open(textFileName, encoding = 'UTF-8').read()
# raw_text = raw_text.lower()
import nltk
import csv
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import stopwords
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names

dummy_data = """Do you know where the fuck you are?
You're in the jungle baby
We got tragedy

Welcome to the jungle
We got fun 'n' games
We got everything you want
Honey we know the names
We are the people that can find
Whatever you may need
If you got the money honey
We got your disease

In the jungle
Welcome to the jungle
Watch it bring you to your shun na na na
Knees, knees
I wanna watch you bleed

Welcome to the jungle
We take it day by day
If you want it, you're gonna bleed
But it's the price you pay
And you're a very sexy girl
Very hard to please
You can taste the bright lights
But you won't get them for free

In the jungle
Welcome to the jungle
Feel my, my, my, my serpentine
Oh , I wanna hear you scream

Welcome to the jungle
It get's worse here everyday
Ya learn to live like an animal
In the jungle where we play
If you got a hunger for what you see
You'll take it eventually
You can have anything you want
But you better not take it from me

In the jungle
Welcome to the jungle
Watch it bring you to your shun na na na
Knees, knees
I wanna watch you bleed

And when you're high you never
Ever wanna come down, so down
Sucked down, so down yeah

You know where you are?
You're in the jungle baby
You're gonna die

In the jungle
Welcome to the jungle
Watch it bring you to your shun na na na
Knees, knees
In the jungle
Welcome to the jungle
Feel my, my, my, my serpentine

In the jungle
Welcome to the jungle
Watch it bring you to your shun na na na
Knees, knees
In the jungle
Welcome to the jungle
Watch it bring you to your
It's gonna bring you down
Ha"""
dummy_data = dummy_data.lower()
words = word_tokenize(dummy_data)
stopWords = set(stopwords.words('english'))
wordsFiltered = []
 
for w in words:
    if w not in stopWords:
        wordsFiltered.append(w)
tagdata = [] 
wordsFiltered = [word for word in wordsFiltered if word.isalpha()]
print(wordsFiltered)
negative_words = open("C:/Users/Kasie/Desktop/python/project-final/static/negative-words.txt", "r")
positive_words = open("C:/Users/Kasie/Desktop/python/project-final/static/positive-words.txt", "r")
negative_word_list = negative_words.read().splitlines()
positive_words_list = positive_words.read().splitlines()

def word_feats(words):
    return dict([(word, True) for word in words])

positive_features = [(word_feats(pos), 'pos') for pos in positive_words_list]
negative_features = [(word_feats(neg), 'neg') for neg in negative_word_list]
train_set = negative_features + positive_features
classifier = NaiveBayesClassifier.train(train_set) 

neg = 0
pos = 0
for word in wordsFiltered:
    classResult = classifier.classify( word_feats(word))
    if classResult == 'neg':
        neg = neg + 1
    if classResult == 'pos':
        pos = pos + 1
 
print('Positive: ' + pos)
print('Negative: ' + neg)

