# import
from xImports import *
from xTools import *
import matplotlib.patheffects as path_effects

# ------------------------------------------------------------------------------

if __name__ == "__main__":
    print( "{:s}: Run main routine instead!".format(__file__) )
    quit()

# ------------------------------------------------------------------------------

def PlotConfusionMatrix( gold_tags, test_tags, title='Confusion matrix', display=True, createPNG=False, PNGfname="result", PNGtransparency=False  ):
    # text output
    cm = ConfusionMatrix(gold_tags, test_tags)    
    print( cm )
    
    accuracy = cm._correct/cm._total
    print( 'Correct: {:d} / Total: {:d} ({:.4f})'.format(cm._correct, cm._total, accuracy) )
    
    # graphic visualization
    cm_data = confusion_matrix(gold_tags, test_tags, labels=universal_tagset)
    num_tags = len(universal_tagset)

    # substract correct tagged from total
    cm_data_scaled = np.copy(cm_data)
    for i in range(0,len(cm_data_scaled)):
        cm_data_scaled[i][i] = 0
    
    plt.clf()
        
    # using Reds colormap
    cmap = plt.cm.Reds

    # normalize data
    norm = plt.Normalize(cm_data_scaled.min(), cm_data_scaled.max())
    rgba = cmap(norm(cm_data_scaled))

    # make diagonal (perfect matches) green
    # zeros to plain white (looks better)
    for y in range(0,num_tags):
        for x in range(0, num_tags):
            if x == y:
                rgba[x, y, :3] = 0,1,0                
            else: 
                if cm_data_scaled[x][y] == 0:
                    rgba[x, y, :3] = 1,1,1

    # plot data and legend
    plt.imshow(rgba, interpolation='nearest')
    im = plt.imshow(cm_data_scaled, visible=False, cmap=cmap)
    plt.colorbar(im)

    # text portion
    ind_array = np.arange(0, num_tags, 1)
    x, y = np.meshgrid(ind_array, ind_array)    
    for x_val, y_val in zip(x.flatten(), y.flatten()):
        c = str(cm_data[y_val][x_val])
        plt.text(x_val, y_val, c, va='center', ha='center', color='black', path_effects=[path_effects.Stroke(linewidth=2, foreground='white'), path_effects.Normal()])


    # add x/y labels
    plt.xlabel( 'predicted' + '\n(Accuracy: {:.4f})'.format(accuracy) )
    plt.ylabel( 'reference' )

    plt.xticks( np.arange(0, num_tags), universal_tagset, rotation=90 )
    plt.yticks( np.arange(0, num_tags), universal_tagset, rotation=0 )
    plt.title( title, y=1.01 )

    # add grid
    plt.grid()

    # fit to screen. ensure everything is visible
    plt.tight_layout()
    
    # save
    if createPNG:    
        fig = plt.gcf()
        fig.set_size_inches(10.0, 10.0)
        fig.savefig( PNGfname, bbox_inches="tight", transparent=PNGtransparency, dpi=300 )
        PrintGreen( "Saved as {:s}".format(PNGfname) )
        
    # show?
    if display:
        plt.show()
