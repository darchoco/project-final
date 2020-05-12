import nltk
import csv
import pandas as pd
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import stopwords
import nltk.classify.util
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import names
negative_words = open("C:/Users/Kasie/Desktop/python/project-final/static/negative-words.txt", "r")
positive_words = open("C:/Users/Kasie/Desktop/python/project-final/static/positive-words.txt", "r")
negative_word_list = negative_words.read().splitlines()
positive_words_list = positive_words.read().splitlines()

# Define class for basic word calculations that contains string of words
class word_calcs:
    negative_words = open("C:/Users/Kasie/Desktop/python/project-final/static/negative-words.txt", "r")
    positive_words = open("C:/Users/Kasie/Desktop/python/project-final/static/positive-words.txt", "r")
    negative_word_list = negative_words.read().splitlines()
    positive_words_list = positive_words.read().splitlines()
    def __init__(self,words):
        self.words = words.lower()


    # Converts string of words into a list of individual words 
    def wordcount(self):
        allwords = word_tokenize(self.words)
        return len(allwords)

    # counts words that remove the stopwords
    def nostopwordcount(self):
        allwords = word_tokenize(self.words)
        stopWords = set(stopwords.words('english'))
        wordsFiltered=[]
        for w in allwords:
            if w not in stopWords:
                wordsFiltered.append(w)
        return len(wordsFiltered)

    # Returns list of words with the stopwords excluded
    def nostopwordlist(self):
        allwords = word_tokenize(self.words)
        stopWords = set(stopwords.words('english'))
        wordsFiltered=[]
        for w in allwords:
            if w not in stopWords:
                wordsFiltered.append(w)
        return wordsFiltered

    # Calculate positive word count, give option to include/exclude stopwords
    def positivewordcount(self, stopwords = False):
        poscount = 0
        if stopwords ==False:
            filteredwords = self.nostopwordlist()
            for word in filteredwords:
                if word in positive_words_list:
                    poscount = poscount+1
            return poscount
        else:
            allwords = word_tokenize(self.words)
            for word in allwords:
                if word in positive_words_list:
                    poscount = poscount+1
            return poscount

        # Calculate positive word count, give option to include/exclude stopwords
    def negativewordcount(self, stopwords = False):
        negcount = 0
        if stopwords ==False:
            filteredwords = self.nostopwordlist()
            for word in filteredwords:
                if word in negative_word_list:
                    negcount = negcount+1
            return negcount
        else:
            allwords = word_tokenize(self.words)
            for word in allwords:
                if word in negative_word_list:
                    negcount = negcount+1
            return negcount

    def neutralwordcount(self, stopwords = False):
        neucount = 0
        if stopwords ==False:
            filteredwords = self.nostopwordlist()
            for word in filteredwords:
                if (word not in negative_word_list and word not in self.positive_words_list):
                    neucount = neucount+1
            return neucount
        else:
            allwords = word_tokenize(self.words)
            for word in allwords:
                if word not in negative_word_list and word not in self.positive_words_list:
                    neucount = neucount+1
            return neucount