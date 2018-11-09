'''
Script for searching for frequent abbreviations in a CONLL like corpus with
existing tags for abbreviations.
When specify a directory, all files in this directory will be read in and will
be analyzed. Output contains the accumulated results of every file.

Writes a list with amount of tokens and abbreviations including the 
abbreviation with their frequency in descending order.
'''

import operator, os

# the file to analyze - or directory
tagged_file = r'''Z:\Abkuerzungen\corpora\...'''
# file which holds the results
output_file = r'''Z:\Abkuerzungen\corpora\....txt'''

# where the actual word token is located in the CONLL like file
word_index = 0
# where the tag for abbreviation is located in the CONLL like file
tag_index = 2

# amount of abbreviations
count_abbr = 0
# amount of words
count_words = 0
# dictionary with the abbreviations and the frequency of every abbreviation
abbreviations = {}

if os.path.isdir(tagged_file):
    for filename in os.listdir(tagged_file):
        print(filename)
        with open(os.path.join(tagged_file, filename), 'r', encoding='utf-8') as file:
            for line in file:
                line = line.replace('\n', '')
                line = line.split('\t')
                if len(line) > 1:
                    word = line[word_index]
                    tag = line[tag_index]
                    count_words += 1            
                    if tag == 'ABBR':
                        count_abbr += 1
                        if word in abbreviations:
                            abbreviations[word] += 1
                        else:
                            abbreviations[word] = 1
else:
    with open(tagged_file, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.replace('\n', '')
            line = line.split('\t')
            if len(line) > 1:
                word = line[word_index]
                tag = line[tag_index]
                count_words += 1            
                if tag == 'ABBR':
                    count_abbr += 1
                    if word in abbreviations:
                        abbreviations[word] += 1
                    else:
                        abbreviations[word] = 1

# sort the dictionary
sorted_abbreviations = sorted(abbreviations.items(), key=operator.itemgetter(1))

with open(output_file, 'w', encoding='utf-8') as fileW:
    fileW.write('='.join(['Anzahl Tokens', str(count_words)]))
    fileW.write('\n')
    fileW.write('='.join(['Anzahl Abkürzung', str(count_abbr)]))
    fileW.write('\n\n')
    for abbr, frequency in list(reversed(sorted_abbreviations)):
        #print(':'.join([str(abbr), str(frequency)]))
        fileW.write('\t'.join([str(abbr), str(frequency)]))
        fileW.write('\n')

            
            