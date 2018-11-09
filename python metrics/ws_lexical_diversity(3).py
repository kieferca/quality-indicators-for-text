# -*- coding: utf-8 -*-
"""
Created on Sat Jan 30 07:14:47 2016
lexical_diversity as described in the NLTK book: https://www.nltk.org/book/ch01.html

"""



#! python



import string
import nltk


   
# ------------------------------------------------------------------------------ 
    

def lexical_diversity(text):
   return (len(set(text)) / len(text))


# --------------------------------------------------------------------------------
   

