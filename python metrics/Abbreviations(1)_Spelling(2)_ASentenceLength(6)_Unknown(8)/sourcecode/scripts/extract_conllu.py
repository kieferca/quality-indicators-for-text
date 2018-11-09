'''
Script for extracting only the specified columns in the 
specified order in a CONLL like text file.
'''


CONLL_U_FILE = r'''C:\..twitter_1.conllu'''
OUTPUT_FILE = r'''C:\..\twitter_1.conllu'''
columns_to_keep_and_order = [1,3,7,10]
# add pseudo tag for abbreviation detection
add_Others_Answer = False

f = open(CONLL_U_FILE, 'r')
fw = open(OUTPUT_FILE, 'w')

for line in f:
    line = line.replace('\n', '')
    columns = line.split('\t')
    if len(columns) > 1:
        new_columns = []
        for column_to_keep in columns_to_keep_and_order:
            new_columns.append(columns[column_to_keep])
        if add_Others_Answer:
            new_columns.append('O')
        columns = new_columns    
        fw.write("\t".join(columns))
    fw.write("\n")
        
f.close()
fw.close()