# -*- coding: utf-8 -*-
"""
Created on Thu Nov  8 16:14:12 2018

 Percentage of uppercased letters
"""

from pickle import load
import nltk
from nltk import word_tokenize


# ------------------------------------------------------------------------------ 

def LoadPickle( fname ):
#    from pickle import load
    f = open('{:s}.pickle'.format(fname), 'rb')
    data = load(f)
    f.close()
    return data
    
# ------------------------------------------------------------------------------ 
    


print( "Measuring corpora '{:s}.pickle'".format("./corpora_pickle/xx") )
tagged_sents = LoadPickle("./corpora_pickle/xx")

#if necessary, tokenize the text string, then only iterate on words
#tokens = word_tokenize(raw)
 
islower_list = [];
isupper_list = [];
word_list = [];

for sent in tagged_sents: 
    for word in sent:      
        if word.islower():
            islower_list.append(word)         
        if word.isupper():
            isupper_list.append(word)         
        word_list.append(word)    
        

print("numbers of words:")
print(str(len(word_list)))

print("islower: "+ str(len(islower_list)/len(word_list)))
print("isupper: "+ str(len(isupper_list)/len(word_list)))
