from xImports import *

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    print( "{:s}: Run main routine instead!".format(__file__) )
    quit()

# ------------------------------------------------------------------------------

def CalcAccuracy( gold, tagged ):
    if len(gold) != len(tagged):
        raise ValueError("Lists must have the same length.")
    return sum(x[1] == y[1] for x, y in zip(gold, tagged)), len(tagged)

# ------------------------------------------------------------------------------ 

def Print( *x, col=colorama.Fore.WHITE, end='\n' ):
    print( colorama.Style.BRIGHT + col, end='' )
    print( *x, end='' )
    print( colorama.Style.RESET_ALL + colorama.Back.RESET, end=end )
    
def PrintGreen( *x, end='\n' ):
    Print( *x, col=colorama.Fore.GREEN, end=end )
def PrintYellow( *x, end='\n' ):
    Print( *x, col=colorama.Fore.YELLOW, end=end )
def PrintRed( *x, end='\n' ):
    Print( *x, col=colorama.Fore.RED, end=end )
def PrintCyan( *x, end='\n' ):
    Print( *x, col=colorama.Fore.CYAN, end=end )
def PrintRedBack( *x, end='\n' ):
    Print( *x, col=colorama.Back.RED, end=end )
def PrintLightRedBack( *x, end='\n' ):
    Print( *x, col=colorama.Back.LIGHTRED_EX, end=end )
    
# ------------------------------------------------------------------------------ 

def SavePickle( data, fname ):
    from pickle import dump
    f = open('{:s}.pickle'.format(fname), 'wb')
    dump(data, f, -1)
    f.close()
    
# ------------------------------------------------------------------------------ 

def LoadPickle( fname ):
    from pickle import load
    f = open('{:s}.pickle'.format(fname), 'rb')
    data = load(f)
    f.close()
    return data
    
# ------------------------------------------------------------------------------ 

def SpellColorizePrint( s, matches ):
    i = 0
    for m in matches:
        PrintGreen( s[i:m.fromx], end='' )
        if i % 2:
            PrintRedBack( s[m.fromx:m.tox], end='' )
        else:
            PrintLightRedBack( s[m.fromx:m.tox], end='' )            
        i = m.tox
    PrintGreen( s[i:] )

# -------------------------------------------------------------------------------

def ShowProgress(count, total, suffix=''):
    bar_len = 32
    filled_len = int(round(bar_len * count / float(total)))

    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)

    sys.stdout.write('[%s] %s%s %s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()
    
# -------------------------------------------------------------------------------

def LangToolSpellCheck( tagged_sents ):
    errors = 0
    num_sents = len(tagged_sents)
    
    for i in range(0, num_sents):  
        ShowProgress(i, num_sents, "LanguageTool")
        
        text = untokenize(untag(tagged_sents[i]))
        matches = lt_check.check(text)
        errors += len(matches)
        
    return errors

# -------------------------------------------------------------------------------

def LangToolSpellCheck2( untagged_sents ):
    errors = 0
    num_sents = len(untagged_sents)
    
    for i in range(0, num_sents):  
        ShowProgress(i, num_sents, "LanguageTool")
        
        text = untokenize(untagged_sents[i])
        matches = lt_check.check(text)
        errors += len(matches)
        
    return errors

# ------------------------------------------------------------------------------ 

def EnchantSpellCheck( tokens, use_is_alpha=False ):
    errors1, errors2, errors3 = 0, 0, 0
    
    num_tokens = len(tokens)
    for i in range(0, num_tokens):        
        ShowProgress(i, num_tokens, "PyEnchant")
        
        t = tokens[i]
        
        # ignore correct tokens
     #   if pe_check.check(t):
      #     continue
        
        # alpha numeric filter
        if (use_is_alpha and not t.isalpha()):
            continue
        
      #  wrongcase = pe_check.check(t.lower())
      #  isunknown = len(pe_check.suggest(t)) == 0

        """
        if isunknown:
            PrintRed( t, wrongcase )
        else:
            if wrongcase:
                PrintGreen( t, wrongcase, pe_check.suggest(t)[0] )
            else:
                PrintYellow( t, wrongcase, pe_check.suggest(t)[0] )
        """
        
        errors1 += 1        
       # if wrongcase:
      #      errors2 += 1
    #    if isunknown:
      #      errors3 += 1
            
    return errors1, errors2, errors3

# ------------------------------------------------------------------------------

def SentsListToWordsList( sents ):
    words = []
    for s in sents:
        for w in s:
            words.append(w)
    return words

# ------------------------------------------------------------------------------

def StopwordTokenCount( tokens ):
    stop_words = set(stopwords.words('english'))
    
    count = 0
    for w in tokens:
        if w.lower() in stop_words:
            count += 1
    return count

# ------------------------------------------------------------------------------

def EvaluatePerceptronTagger( gold_words ):
    # load pretrained
    apt_tagger = PerceptronTagger(load=True)
    
    # eval apt
    tagged_words = apt_tagger.tag( untag(gold_words) )
    tagged_words = [(token, nltk.tag.map_tag('en-ptb', CONST_tagset, tag)) for (token, tag) in tagged_words]
    result, length = CalcAccuracy( gold_words, tagged_words )
    result = result / length
    return result

# ------------------------------------------------------------------------------ 

def UniqueTokenCount( tokens ):
    # frequency distribution
    words_fdist = nltk.FreqDist( tokens )
    less_common = list(reversed(words_fdist.most_common())) 
    
    # words that occur only once 
    count = 0
    words = []
    for i in range(0, len(less_common)):
        if less_common[i][1] > 1:
            break
        words.append(less_common[i][0])
        count += 1
    return count, words

# -------------------------------------------------------------------------------

def PrecisionAndRecallFromConfusionMatrix( cm ):
    cm_sums = []
    num_rows = len(cm._confusion)
    
    # sum total reference 
    for r in range(0,num_rows):
        i = 0
        for c in range(0,num_rows):
            i += cm._confusion[r][c]
        cm_sums.append([i, -1])
    
    # sum total predicted
    for c in range(0,num_rows):
        i = 0
        for r in range(0,num_rows):
            i += cm._confusion[r][c]
        cm_sums[c][1] = i
    
    # calc f-score
    results = []
    for r in range(0,num_rows):
        precis = cm._confusion[r][r] / cm_sums[r][1]
        recall = cm._confusion[r][r] / cm_sums[r][0]
        results.append( [precis, recall] )
        
    return results

# -------------------------------------------------------------------------------

def CountUnknownWords( tagged_words ):
    # need tupples
    if isinstance(tagged_words[0], tuple):
       
        result = 0
        for w in tagged_words:
            if w[1] == 'X':
                result += 1
        return result

    return -1
# ------------------------------------------------------------------------------ 

def CountAbbreviations( tagged_words ):
    result = 0
    for w in tagged_words:
        if len(w[0]) > 1 and w[0].endswith( '.' ):
            result += 1
    return result    

# ------------------------------------------------------------------------------ 

def WriteToFile( fname, data ):
    file = open( fname, 'w')
    file.write( data )
    file.close()    

# ------------------------------------------------------------------------------ 

def ReadFromFile( fname ):
    file = open( fname, 'r')
    data = file.read()
    file.close()   
    return data
	
# ------------------------------------------------------------------------------

def untokenize(words):
    """
    Source: https://github.com/commonsense/metanl/blob/master/metanl/token_utils.py
    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.
    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    """
    text = ' '.join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace("can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    step7 = step6.replace("$ ", "$") # added
    return step7.strip()

# ------------------------------------------------------------------------------

def SecondsToTimeString( secs ):
    h = int(secs / (60 * 60))
    m = int((secs % (60 * 60)) / 60)
    s = secs % 60.
    return "{:>02}:{:>02}:{:>02.0f}".format(h, m, s)

# ------------------------------------------------------------------------------

def TableDataToCSV( table_data ):
    csv_data = "" 
    for row in table_data:
        # ignore 1st column (description)
        for i in range(1, len(row) ):
            csv_data += row[i].replace('.',',')
            if i < len(row) - 1:
                csv_data += ";"
        csv_data += "\n"
    return csv_data

# -------------------------------------------------------------------------------

def TwitterTagToUniversal( tag ):
    twict = { 
        '!':'PRT',  '#':'X', '   $':'NUM',  '&':'CONJ', ',':'.',    '@':'X',    
        'A':'ADJ',  'D':'DET',  'E':'X',    'G':'X',    'L':'PRT',  'M':'PRT',
        'N':'NOUN', 'O':'PRON', 'P':'ADP',  'R':'ADV',  'S':'NOUN', 'T':'PRT',
        'U':'X',    'V':'VERB', 'X':'PRT',  'Y':'PRT',  'Z':'NOUN', '^':'NOUN', '~':'X'
    }
    return twict[tag]
