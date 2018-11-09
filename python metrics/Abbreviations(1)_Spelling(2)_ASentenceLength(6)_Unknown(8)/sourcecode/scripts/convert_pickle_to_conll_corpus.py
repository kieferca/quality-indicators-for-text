from pickle import load
fname = '''Z:/.../....low'''
f = open('{:s}.pickle'.format(fname), 'rb')
data = load(f)
f.close()

with open('''C:/Users/.../....conll''', 'w', encoding='UTF-8') as file:
    i = 0
    for tagged_post in data:          
        for word_tag in tagged_post:
            if isinstance(word_tag, str):
                i += 1
                file.write(word_tag)
                file.write('\n')
            else:  
                i += 1
                file.write('\t'.join(word_tag))
                file.write('\n')
        file.write('\n')