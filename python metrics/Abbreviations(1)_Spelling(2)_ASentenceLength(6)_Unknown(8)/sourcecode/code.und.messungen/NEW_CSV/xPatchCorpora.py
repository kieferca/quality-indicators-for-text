# import
from xImports import *
from xTools import *

# -------------------------------------------------------------------------------

def PatchCorpora( corpora_fname, method_flag ):
    bLowerCase     = (method_flag & pow(2,0)) > 0
    bCorrectTokens = (method_flag & pow(2,1)) > 0
    bCorrectWords  = (method_flag & pow(2,2)) > 0
    bRemoveSwords  = (method_flag & pow(2,3)) > 0
      
    methods = ""
    if bRemoveSwords:
        methods += ".nsw"  
    if bLowerCase:
        methods += ".low"
    if bCorrectTokens:
        methods += ".cot"
    if bCorrectWords:
        methods += ".cow"

    PrintYellow( "Patching corpora: '{:s}.pickle'. Patches: '{:s}'.".format(corpora_fname, methods) )

    sents = LoadPickle( corpora_fname )
    stop_words = set(stopwords.words('english'))    
 
    result = []    
    num_sents = len(sents)
    
    for i in range(0, num_sents): 
        ShowProgress(i, num_sents, "PatchCorpora")
        
        sent = []
        for word in sents[i]:
            if isinstance(word, str):
                w = word
            else:
                w = word[0]
            
            # remove stopwords
            if bRemoveSwords and w.lower() in stop_words:
                continue
                
            # correct
         #   if (bCorrectTokens or bCorrectWords) and not pe_check.check(w):
         #       if (bCorrectWords and w.isalpha()) or bCorrectTokens:
          #          wnew = pe_check.suggest(w)
           #         if len(wnew) > 0:
            #            w = wnew[0]
                        
            # lower case
            if bLowerCase:
                w = w.lower()

            if isinstance(w, str):
                sent.append(w)
            else:
                sent.append( (w, word[1]) )
            
        result.append(sent)
        
    print("")
    SavePickle( result, "{:s}{:s}".format(corpora_fname, methods) )    
    PrintGreen( "Saving as {:s}{:s}.pickle".format(corpora_fname, methods) )