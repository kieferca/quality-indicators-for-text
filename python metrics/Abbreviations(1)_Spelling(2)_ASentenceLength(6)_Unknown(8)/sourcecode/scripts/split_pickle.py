'''
Script for splitting one given pickle corpus to many smaller ones. 
'''

import os
from pathlib import Path

input_dir = r'''C:\...''' 
output_dir = r'''C:\...'''

def SavePickle( data, fname ):
    from pickle import dump
    f = open('{:s}.pickle'.format(fname), 'wb')
    dump(data, f, -1)
    f.close()

def LoadPickle( fname ):
    from pickle import load
    f = open('{:s}.pickle'.format(fname), 'rb')
    data = load(f)
    f.close()
    return data
    
def split_list(alist, wanted_parts=1):
    length = len(alist)
    return [ alist[i*length // wanted_parts: (i+1)*length // wanted_parts] 
             for i in range(wanted_parts) ]

length_sents = 0
for file in os.listdir(input_dir):
    name_counter = 0
    if file.endswith(".low.pickle"):
        pickle = file.replace('.pickle', '')
        sents = LoadPickle(os.path.join(input_dir, pickle))
        # c-style division
        # every part should contain of around 250000 tokens.
        wanted_parts = len(sents) // 250000
        sents_split = split_list(sents, wanted_parts)
        pickle = pickle.replace('.low', '')
        for sents_part in sents_split:
            output_pickle = os.path.join(output_dir, pickle + str(name_counter) + '.low')
            pickle_file = Path(output_pickle + '.pickle')
            while pickle_file.exists():
                name_counter += 1
                output_pickle = os.path.join(output_dir, pickle + str(name_counter) + '.low')
                pickle_file = Path(output_pickle + '.pickle')
            SavePickle(sents_part, output_pickle)
            length_sents += len(sents_part)
            print(output_pickle)
            print(len(sents_part))
            print('___________')
print(length_sents)