# import
from xImports import *
from xTools import *
from xAbbreviationDetection import CountAbbreviations2

# -------------------------------------------------------------------------------

def MeasureCorpora( corpora_fname ):

    PrintYellow( "Measuring corpora '{:s}.pickle'".format(corpora_fname) )
    tagged_sents = LoadPickle( corpora_fname )
    tagged_words = SentsListToWordsList( tagged_sents )
    if isinstance(tagged_words[0], tuple):
        untagged_words = untag(tagged_words)
    else:
        untagged_words = tagged_words
   
    # enumerate stats
    num_sents = len(tagged_sents)
    num_words = len(tagged_words)
    num_diffwords = len(set(untagged_words))
    num_uniquewords = UniqueTokenCount(untagged_words)
    num_stopwords = StopwordTokenCount(untagged_words)
    num_unknown = CountUnknownWords(tagged_words)

    # count the abbreviations with crfs and Stanford NER
    if len(sys.argv) >= 4:
        num_abbrev = CountAbbreviations2(tagged_sents, sys.argv[3])
    else:
        num_abbrev = CountAbbreviations2(tagged_sents)

    # spell check
#    num_pe_errors, num_pe_errcase, num_pe_unknown = EnchantSpellCheck(untagged_words)
#    num_lt_errors = LangToolSpellCheck(tagged_sents)

    num_pe_errcase = -1
    num_pe_unknown = -1
    num_pe_errors = -1
    num_lt_errors = -1

    # eval. tagger
    if isinstance(tagged_words[0], tuple):
        num_accuracy = EvaluatePerceptronTagger(tagged_words)
    else:
        num_accuracy = -1

    # calc. accuracy
    num_noise_pe = num_pe_errors / num_words
    num_noise_lt = num_lt_errors / num_words
    num_noise_uk = num_unknown / num_words
    
    # build table
    table_data = [
        ['corpus', 'sents', 'tokens', 'different', 'unique', 'stopwords', 'unknown', 'abbrev', 'pe_errall', 'pe_errcase', 'pe_unknown', 'lt_errors', 'accuracy', 'noise_pe', 'noise_lt', 'noise_uk' ],
        [     '-',     '-',      '-',         '-',      '-',         '-',       '-',      '-',         '-',          '-',          '-',         '-',        '-',        '-',        '-',       '-', ],
    ] 

    # set values
    table_data[1][ 0] = corpora_fname
    table_data[1][ 1] = '{:d}'.format(num_sents)
    table_data[1][ 2] = '{:d}'.format(num_words)
    table_data[1][ 3] = '{:d}'.format(num_diffwords)
    table_data[1][ 4] = '{:d}'.format(num_uniquewords[0])
    table_data[1][ 5] = '{:d}'.format(num_stopwords)
    table_data[1][ 6] = '{:d}'.format(num_unknown)
    table_data[1][ 7] = '{:d}'.format(num_abbrev)
    table_data[1][ 8] = '{:d}'.format(num_pe_errors)
    table_data[1][ 9] = '{:d}'.format(num_pe_errcase)
    table_data[1][10] = '{:d}'.format(num_pe_unknown)
    table_data[1][11] = '{:d}'.format(num_lt_errors)
    table_data[1][12] = '{:f}'.format(num_accuracy)
    table_data[1][13] = '{:f}'.format(num_noise_pe)
    table_data[1][14] = '{:f}'.format(num_noise_lt)
    table_data[1][15] = '{:f}'.format(num_noise_uk)


    # print asci table
    table = AsciiTable(table_data)
    PrintGreen(table.table)
    
    csv_data = TableDataToCSV(table_data)    
    WriteToFile( "{:s}.csv".format(corpora_fname), csv_data )
    PrintGreen( "Saved results as {:s}.csv".format(corpora_fname) )
    
    return