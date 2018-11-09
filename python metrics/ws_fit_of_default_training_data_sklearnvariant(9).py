# -*- coding: utf-8 -*-
"""
Created on Wed Oct 31 08:45:46 2018
Data quality indicators for text: fit of (default) training data

"""

#! python
import nltk

from nltk.corpus import treebank
from nltk.corpus import brown
from nltk.corpus import nps_chat
from nltk.corpus import conll2000

import string
from sklearn.feature_extraction.text import TfidfVectorizer


#corpora 
brown = brown.raw()
nps_chat = nps_chat.raw()
conll2000 = conll2000.raw()
treebank = treebank.raw()

default=treebank;
operational= brown;

stemmer = nltk.stem.porter.PorterStemmer()
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


def stem_tokens(tokens):
    return [stemmer.stem(item) for item in tokens]


def tokenize(text):
    return (nltk.word_tokenize(text.lower()))

'''lowercase, stem'''
def normalize_leave_punctuation(text):
    return stem_tokens(nltk.word_tokenize(text.lower()))

'''remove punctuation, lowercase, stem'''
def normalize(text):
    return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

'''remove punctuation, lowercase, no stemming!'''
def normalize_no_stemming(text):
    return (nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))
    

vectorizer = TfidfVectorizer(tokenizer=tokenize, stop_words='english')

def cosine_sim(text1, text2):
    tfidf = vectorizer.fit_transform([text1, text2])
    return ((tfidf * tfidf.T).A)[0,1]


print(cosine_sim(default, operational))

