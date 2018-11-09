'''
Merge pickle files.
'''

import os

input_dir = r'''Z:\...'''
output_pickle = r'''Z:\...'''

def LoadPickle( fname ):
    from pickle import load
    f = open('{:s}'.format(fname), 'rb')
    data = load(f)
    f.close()
    return data

def SavePickle( data, fname ):
    from pickle import dump
    f = open('{:s}.pickle'.format(fname), 'wb')
    dump(data, f, -1)
    f.close()
    
sentences = []
for file in os.listdir(input_dir):
    if file.endswith(".low.pickle"):
        if not file == output_pickle:
            print(file)
            data = LoadPickle(os.path.join(input_dir, file))
            sentences.extend(data)
                                
SavePickle(sentences, output_pickle)
