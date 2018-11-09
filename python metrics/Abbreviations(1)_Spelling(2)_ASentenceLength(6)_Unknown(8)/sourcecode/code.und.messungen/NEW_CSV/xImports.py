# import NLTK
import nltk
# import TnT taggers
from nltk.tag import untag, tnt
# import average perceptron tagger
from nltk.tag.perceptron import PerceptronTagger
# import corpus
from nltk.corpus import brown, treebank, conll2000, nps_chat
# import stopwords
from nltk.corpus import stopwords
# import tokenizers
# tokenize sents
from nltk.tokenize.punkt import PunktSentenceTokenizer, PunktParameters
# tokenize words
from nltk.tokenize import TreebankWordTokenizer, RegexpTokenizer
# twitter tokenizer
# from twokenize import tokenize as twokenize
# import dictionary
# import enchant
# import console coloring
import colorama
# import edit distance
from nltk.metrics import edit_distance
# plot
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.axes_grid1 import make_axes_locatable
#
import pylab
import numpy as np
# grammar
import language_check
# ascii tables
from terminaltables import AsciiTable
# confusion matrix
from nltk.metrics import ConfusionMatrix
from sklearn.metrics import confusion_matrix
# system related
import os
import sys
import threading
from winsound import Beep
from time import sleep
# untokenize
import re
# runtime measurement
import timeit
#
import csv

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    print("{:s}: Run main routine instead!".format(__file__))
    quit()

# ------------------------------------------------------------------------------

# init colorama
colorama.init()

# global constants
CONST_tagset = 'universal'

# global list of gold corpora
# C:\Users\admin\AppData\Roaming\nltk_data\corpora\
corp_names = ["brown", "nps_chat", "conll2000", "treebank", "twitter", "nhtsa_0", "nhtsa_1", "nhtsa_2", "nhtsa_3",
              "nhtsa_4", "nhtsa_5", "nhtsa_6"]
corp_words_tagged = [brown.tagged_words(tagset=CONST_tagset), nps_chat.tagged_words(tagset=CONST_tagset),
                     conll2000.tagged_words(tagset=CONST_tagset), treebank.tagged_words(tagset=CONST_tagset)]
corp_words_untagged = [brown.words(), nps_chat.words(), conll2000.words(), treebank.words()]
corp_sents_tagged = [brown.tagged_sents(tagset=CONST_tagset), nps_chat.tagged_posts(tagset=CONST_tagset),
                     conll2000.tagged_sents(tagset=CONST_tagset), treebank.tagged_sents(tagset=CONST_tagset)]
corp_sents_untagged = [brown.sents(), nps_chat.posts(), conll2000.sents(), treebank.sents()]

# language tool spell checker
lt_check = language_check.LanguageTool('en-US')

# pyenchant spell checker
# pe_check = enchant.Dict('en_US')

universal_tagset = ['.', 'ADJ', 'ADP', 'ADV', 'CONJ', 'DET', 'NOUN', 'NUM', 'PRON', 'PRT', 'VERB', 'X']
