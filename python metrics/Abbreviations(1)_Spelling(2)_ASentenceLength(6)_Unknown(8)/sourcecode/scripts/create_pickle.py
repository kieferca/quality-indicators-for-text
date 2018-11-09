'''
Script for creating a pickle file out of a CONLL like text file.
'''

input_file = r'''..'''
output_pickle = r'''..'''

def SavePickle( data, fname ):
    from pickle import dump
    f = open('{:s}.pickle'.format(fname), 'wb')
    dump(data, f, -1)
    f.close()
    
sentences = []
with open(input_file, 'r', encoding='utf8') as file:
    sent = []
    for line in file:
        line = line.replace('\n', '')
        line = line.split('\t')
        if len(line) > 1:
            sent.append(line[0])
        else:
            sentences.append(sent)
            sent = []
            
SavePickle(sentences, output_pickle)

