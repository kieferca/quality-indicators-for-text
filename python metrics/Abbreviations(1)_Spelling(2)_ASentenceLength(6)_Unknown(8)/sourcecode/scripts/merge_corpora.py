'''
Script for merging all corpora in a given folder.
'''

import os

input_folder = r'''C:\...\...'''
output_file = r'''..'''


with open(os.path.join(input_folder, output_file), 'w', encoding='utf-8') as fileW:
    for file in os.listdir(input_folder):
        if not file.endswith(".conllu"):
            if not file == output_file:
                print(file)
                with open(os.path.join(input_folder, file), 'r', encoding='utf-8') as fileR:
                    for line in fileR:
                        fileW.write(line)
                        