import subprocess
from pathlib import Path
from xUniversalTagsCreator import conll_create_universal_tagging
import os


def ShrinkConllU(input_file, columns_to_keep_and_order, add_Others_Answer=False):
    """
    Method for shrinking tab separated CONLL files. It will save to the input_file
    It is mainly used because Stanford CoreNLP saves more annotation than is used for the
    Stanford NER model.

    :param input_file: the file to shrink and saving location
    :param columns_to_keep_and_order: the columns to keep and the order for saving the columns
    :param add_Others_Answer: should also be a new row written with fake gold answers.
    """

    # reads the CONLL file
    input = []
    with open(input_file, 'r', encoding='utf8') as file:
        sent = []
        for line in file:
            line = line.replace('\n', '')
            line = line.split('\t')
            if len(line) > 1:
                sent.append(line)
            else:
                input.append(sent)
                sent = []

    # shrink the CONLL file
    with open(input_file, 'w', encoding='utf8') as file:
        for sent in input:
            for columns in sent:
                if len(columns) > 1:
                    new_columns = []
                    for column_to_keep in columns_to_keep_and_order:
                        new_columns.append(columns[column_to_keep])
                    if add_Others_Answer:
                        new_columns.append('O')
                    columns = new_columns
                    file.write('\t'.join(columns))
                    file.write('\n')
            file.write('\n')


def CountAbbreviations2(tagged_sents, language='english'):
    """
    This is a new method for counting the abbreviations using conditional random fields including in
    Stanford NER.
    For pos tagging and dependency parsing Stanford CoreNLP is used.

    @:param tagged_sents: the sentences in which abbreviations will be searched.
    @:param language: The language of the sentences. Only 'english' and 'german' are supported.

    @:return: the amount of found abbreviations in tagged_sents
    """

    # path of the script
    current_dir_path = os.path.dirname(os.path.realpath(__file__))

    # choosing the property file for Stanford CoreNLP according to the give language param.
    if language is None:
        language = 'english'
    if language.lower() == 'english':
        props_file = os.path.join(os.path.join(current_dir_path, '''StanfordCoreNLP'''), '''StanfordCoreNLP-english.properties''')
    elif language.lower() == 'german':
        props_file = os.path.join(os.path.join(current_dir_path, '''StanfordCoreNLP'''), '''StanfordCoreNLP-german.properties''')

    # define the directories in which the temporary files will be saved
    temp_dir = os.path.join(current_dir_path, 'TEMP')
    temp_file = os.path.join(temp_dir, 'corpus')

    # define the Stanford CoreNLP and Stanford NER jar
    stanford_core_nlp_jar = os.path.join(os.path.join(current_dir_path, '''StanfordCoreNLP'''), 'stanford_core_nlp_custom_document_reader_and_whitespace_lexer.jar')
    stanford_ner_jar = os.path.join(os.path.join(current_dir_path, '''StanfordNER'''), 'stanford_ner.jar')
    # define the CRF model for Stanford NER.
    stanford_ner_model = os.path.join(os.path.join(current_dir_path, '''StanfordNER'''), 'ner-model-abbr-detection.ser.gz')

    # create temp dir if it not exists
    if not os.path.exists(temp_dir):
        os.makedirs(temp_dir)

    # specifies the name ending of the temp file. The ending will be a incrementing number so no older
    # temp file will be overwritten.
    k = 0
    while Path(temp_file + str(k)).exists():
        k += 1
    temp_file = temp_file + str(k)

    # Tab separated file with pos tagged dependency parsed annotation.
    depparse_file = temp_file + '.conllu'

    # The command line argument for running Stanford CoreNLP.
    stanford_core_nlp_command = ["java", "-Xmx45g", "-jar", stanford_core_nlp_jar, "-props", props_file,
                                 "-file", temp_file, "-outputDirectory", temp_dir, "-encoding", "UTF-8"]

    # The command line argument for running Stanford NER.
    stanford_ner_command = ["java", "-jar", stanford_ner_jar, "-Xmx45g", "-cp", ''"*;lib/*"'', "-loadClassifier",
                            stanford_ner_model, "-outputFormat", "tabbedEntities",
                            "-testFile", depparse_file, ">", temp_file, "-encoding", "UTF-8"]

    # first the corpora will be written to the temp file.
    with open(temp_file, 'w', encoding='utf-8') as file:
        for sent in tagged_sents:
            if isinstance(sent[0], str):
                file.write('\t'.join([w for w in sent]))
            else:
                file.write('\t'.join([w[0] for w in sent]))
            file.write('\n')

    # then the written corproa will be dependency parsed with Dtanford CoreNLP
    subprocess.call(stanford_core_nlp_command, shell=True)

    # if the language is english, Stanford CoreNLP uses the Penn Treebank Postags.
    # Universal POS tags will be added.
    if language == 'english':
        # annotate with universal Tags
        conll_create_universal_tagging(depparse_file)

    if language == 'german':
        # Shrink conll-u and add fake gold ner tags
        ShrinkConllU(depparse_file, [1, 4, 7], True)
    else:
        # Shrink conll-u and add fake gold ner tags
        ShrinkConllU(depparse_file, [1, 3, 7], True)

    # actual ner tagging
    subprocess.call(stanford_ner_command, shell=True)

    # Read from the temp file all ABBR annotation and counts it.
    result = 0
    with open(temp_file, 'r', encoding='utf-8') as result_ner:
        for line in result_ner:
            line = line.replace('\n', '')
            line = line.split('\t')
            if len(line) > 1:
                word, ner_tag = line[0], line[2]
                if ner_tag == 'ABBR':
                    result += 1

    return result
