# import
from xImports import *
from xTools import *
from xMeasureCorpora import *
from xPatchCorpora import *
from xPlotConfusionMatrix import *
from recallPrecision import *

# -------------------------------------------------------------------------------

prog_start = timeit.default_timer()
#os.system('@cls')
#os.system('@chcp 65001')

# -------------------------------------------------------------------------------

if len(sys.argv) < 3:
    PrintRed('Not enough arguments! Usage: xPlot <corpora>.pickle <"Title">')
    quit()
    
    
fname = sys.argv[1]
title = sys.argv[2]
showplot = False

gold_sents = LoadPickle( fname )
#gold_sents = gold_sents[:100]
gold_words = sum( gold_sents, [] )

apt_tagger = PerceptronTagger(load=True)

tagged_words = apt_tagger.tag( untag(gold_words) )
tagged_words = [(token, nltk.tag.map_tag('en-ptb', CONST_tagset, tag)) for (token, tag) in tagged_words]

#PrintYellow(gold_words)
#Print(tagged_words)



gold_tags = [ t for (w,t) in gold_words ]
test_tags = [ t for (w,t) in tagged_words ]

PlotConfusionMatrix(gold_tags, test_tags, title=title, display=showplot, createPNG=True, PNGtransparency=True, PNGfname = fname + ".plot.png")

# text output
cm = ConfusionMatrix(gold_tags, test_tags)
# Print(cm)
prlist = PrecisionAndRecallFromConfusionMatrix(cm)
#Print(prlist)

plt = plotPrecisionRecallDiagram(title, np.array(prlist), cm._values)
#plt.show()

# save
plt.savefig( fname + ".fscore.png", bbox_inches="tight", transparent=True )
PrintGreen( "Saved as {:s}".format( fname + ".fscore.png") )
if showplot:
    plt.show()
