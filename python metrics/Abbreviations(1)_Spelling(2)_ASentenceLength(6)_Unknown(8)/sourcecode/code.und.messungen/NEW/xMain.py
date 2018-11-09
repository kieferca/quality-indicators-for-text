# import
from xImports import *
from xTools import *
from xMeasureCorpora import *
from xPatchCorpora import *

# -------------------------------------------------------------------------------

prog_start = timeit.default_timer()
#os.system('@cls')
#os.system('@chcp 65001')


# -------------------------------------------------------------------------------

def Terminate():
    Print( "\nProgram terminated (Runtime: {:s})".format(SecondsToTimeString(timeit.default_timer() - prog_start)) )
    quit()

# -------------------------------------------------------------------------------

def ListCorpora():
    PrintYellow( "Available corpora:")
    for i in range(0, len(corp_names)):
        Print( "  {:2d} -> {:s}".format(i, corp_names[i]) )

# -------------------------------------------------------------------------------

def ShowOptions():
    Print( "Usage: {:s} <task>".format(os.path.basename(__file__)) )
    Print( "Tasks:" )
    Print( "  Show a list of available corpora...: <lc>" )
    Print( "  Measure corpora....................: <mc> <corpora filename>" ) 
    Print( "  Patch corpora......................: <pc> <corpora filename> <patchid>" )
    Print( "                                       <patchid>" )
    Print( "                                           1 - low - lowercase everything" )
    Print( "                                           2 - cot - correct all tokens with PyEnchant" )
    Print( "                                           4 - cow - correct only words(=alphabetic tokens) with PyEnchant" )
    Print( "                                           8 - nsw - remove all stopwords" )
    Print( "                                         Any combination of these: Use sum." )

# -------------------------------------------------------------------------------

def RunMain():
    # 0 args
    if len(sys.argv) == 1:
        ShowOptions()
        return

    # 0 args
    if sys.argv[1].lower() == "lc":
        ListCorpora()

    # 1 arg
    if sys.argv[1].lower() == "mc":
        MeasureCorpora(sys.argv[2])

    # 2 args
    if sys.argv[1].lower() == "pc":
        result = PatchCorpora(sys.argv[2], int(sys.argv[3]))

# ===============================================================================

try:
    RunMain()
	
except:
    PrintRed("Exception:", sys.exc_info()[0])
    PrintRed("Press ENTER to continue...")
    input()

# ===============================================================================

Terminate()