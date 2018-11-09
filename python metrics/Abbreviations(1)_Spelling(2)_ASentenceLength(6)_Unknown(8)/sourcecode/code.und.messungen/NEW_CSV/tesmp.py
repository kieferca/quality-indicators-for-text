import signal
import subprocess
from pathlib import Path

from nltk import LazyConcatenation, LazyMap, map_tag

import os
from nltk.parse.corenlp import CoreNLPDependencyParser
import time
from nltk.corpus import ConllCorpusReader

def DetectAbbreviationFreeFormText(text, language='english'):
    # path of the script
    current_dir_path = os.path.dirname(os.path.realpath(__file__))
    print(current_dir_path)

    # define the directories in which the temporary files will be saved
    temp_dir = os.path.join(current_dir_path, 'TEMP')
    temp_file = os.path.join(temp_dir, 'corpus')

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


    # define the Stanford CoreNLP and Stanford NER jar
    stanford_core_nlp_jar = os.path.join(os.path.join(current_dir_path, '''StanfordCoreNLP'''), 'stanford_core_nlp_custom_document_reader_and_whitespace_lexer.jar')
    stanford_ner_jar = os.path.join(os.path.join(current_dir_path, '''StanfordNER'''), 'stanford_ner.jar')
    # define the CRF model for Stanford NER.
    stanford_ner_model = os.path.join(os.path.join(current_dir_path, '''StanfordNER'''), 'ner-model-abbr-detection.ser.gz')


    # choosing the property file for Stanford CoreNLP according to the give language param.
    if language is None:
        language = 'english'
    if language.lower() == 'english':
        props_file = os.path.join(os.path.join(current_dir_path, '''StanfordCoreNLP'''), '''StanfordCoreNLP-english_CSV.properties''')
    elif language.lower() == 'german':
        props_file = os.path.join(os.path.join(current_dir_path, '''StanfordCoreNLP'''), '''StanfordCoreNLP-german_CSV.properties''')


    stanford_core_nlp_server_command = ["java", "-Xmx45g", "-cp", stanford_core_nlp_jar, "edu.stanford.nlp.pipeline.StanfordCoreNLPServer",
                                        "-serverProperties", props_file,
                                 "-port", "9000", "-timeout", "15000"]

    # The command line argument for running Stanford NER.
    stanford_ner_command = ["java", "-jar", stanford_ner_jar, "-Xmx45g", "-cp", ''"*;lib/*"'', "-loadClassifier",
                            stanford_ner_model, "-outputFormat", "tabbedEntities",
                            "-testFile", depparse_file, ">", temp_file, "-encoding", "UTF-8"]
    print('abbr')

    STANFORD_CORENLP_PROCESS = None
    if STANFORD_CORENLP_PROCESS is None:

        STANFORD_CORENLP_PROCESS = subprocess.Popen(
            stanford_core_nlp_server_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            
        )
        time.sleep(10)
    print('abbr')
    
    STANFORD_CORENLP_PROCESS.kill()
    STANFORD_CORENLP_PROCESS = None
    
DetectAbbreviationFreeFormText('This is an example')