'''
Script for splitting one corpus into a training and test corpus.
'''

import os

input_folder = r'''C:\..'''
output_file_training = '''training_corpora.conllu'''
output_file_testing = '''testing_corpora.conllu'''

modulo = 10
modulo_training = [2,3,4,5,6,7,8,9]
modulo_testing = [0,1]

with open(os.path.join(input_folder, output_file_training), 'w', encoding='utf-8') as fileW:
    with open(os.path.join(input_folder, output_file_testing), 'w', encoding='utf-8') as fileWT:
        for file in os.listdir(input_folder):
            if file.endswith(".conllu"):
                if not file == output_file_training:
                    if not file == output_file_testing:
                        with open(os.path.join(input_folder, file), 'r', encoding='utf-8') as fileR:
                            sentences = []
                            sentence = []
                            for line in fileR:
                                line = line.replace('\n', '')
                                if len(line) > 0:
                                    sentence.append(line)
                                else:
                                    sentences.append(sentence)
                                    sentence = []
                         
                            i = 0
                            amount_training = 0
                            amount_testing = 0
                            while i < len(sentences):
                                if i % modulo in modulo_training:
                                    fileW.write('\n'.join(sentences[i]))
                                    fileW.write('\n\n')
                                    amount_training += 1
                                elif i % modulo in modulo_testing:
                                    fileWT.write('\n'.join(sentences[i]))
                                    fileWT.write('\n\n')
                                    amount_testing += 1
                                i += 1
                            print(amount_training)
                            print(amount_testing)
                            print(len(sentences))
                            print('----------------')
                            