# -*- coding: utf-8 -*-
"""
Script to plot recall-precision values with f-measure equi-potential lines.
Created on Dec 16, 2009
@author: Jörn Hees
"""
# source: https://joernhees.de/blog/2010/07/22/precision-recall-diagrams-including-fmeasure/
# ported to python 3, slightly changed, shrinked

import scipy as sc
import pylab as pl
import itertools as it

def fmeasure(p, r):
    """Calculates the fmeasure for precision p and recall r."""
    return 2*p*r / (p+r)

def _fmeasureCurve(f, p):
    """For a given f1 value and precision get the recall value.

    The f1 measure is defined as: f(p,r) = 2*p*r / (p + r).

    If you want to plot "equipotential-lines" into a precision/recall diagramm
    (recall (y) over precision (x)), for a given fixed f value we get this
    function by solving for r:
    """
    return f * p / (2 * p - f)

def _plotFMeasures(fstepsize=.1, stepsize=0.001):
    """Plots 10 fmeasure Curves into the current canvas."""
    p = sc.arange(0., 1., stepsize)[1:]
    for f in sc.arange(0., 1., fstepsize)[1:]:
        points = [(x, _fmeasureCurve(f, x)) for x in p
                  if 0 < _fmeasureCurve(f, x) <= 1.5]
        xs, ys = zip(*points)
        curve, = pl.plot(xs, ys, "--", color="gray", linewidth=0.5)  # , label=r"$f=%.1f$"%f) # exclude labels, for legend
        # bad hack:
        # gets the 10th last datapoint, from that goes a bit to the left, and a bit down
        pl.annotate(r"$f=%.1f$" % f, xy=(xs[-10], ys[-10]), xytext=(xs[-10] - 0.06, ys[-10] - 0.035), size="small", color="gray")

def _contourPlotFMeasure():
    delta = 0.01
    x = sc.arange(0.,1.,delta)
    y = sc.arange(0.,1.,delta)
    X,Y = sc.meshgrid(x,y)
    cs = pl.contour(X,Y,fmeasure,sc.arange(0.1,1.0,0.1)) # FIXME: make an array out of fmeasure first
    pl.clabel(cs, inline=1, fontsize=10)

def plotPrecisionRecallDiagram(title="title", points=None, labels=None, loc="center right", verbose=False):
    """Plot (precision,recall) values with 10 f-Measure equipotential lines.

    Plots into the current canvas.
    Points is a list of (precision,recall) pairs.
    Optionally you can also provide labels (list of strings), which will be
    used to create a legend, which is located at loc.
    """
    
    pl.clf()
    
    colors = "bgrcmyk"  # 7 is a prime, so we'll loop over all combinations of colors and markers, when zipping their cycles
    markers = "so^>v<dph8"  # +x taken out, as no color.

    if labels:
        ax = pl.axes([0.1, 0.1, 0.7, 0.8])  # llc_x, llc_y, width, height
    else:
        ax = pl.gca()
    pl.title(title)
    pl.xlabel("Precision")
    pl.ylabel("Recall")
    _plotFMeasures()

    #_contourPlotFMeasure()

    if points.any():
        
        getColor = it.cycle(colors)
        getMarker = it.cycle(markers)

        scps = []  # scatter points
        for i, (x, y) in enumerate(points):  
            
            # precision not available (no values)
            if x < 0:
                continue
            
            label = None
            if labels:
                label = labels[i]
                
            if verbose:
                print( "{:6s} p: {:.3f} r: {:.3f} f: {:.3f}".format(label, x, y, fmeasure(x,y)) )
           
            scp = ax.scatter(x, y, label=label, s=50, linewidths=0.75, facecolor=next(getColor), alpha=0.75, marker=next(getMarker) )
            scps.append(scp)
            # pl.plot(x,y, label=label, marker=getMarker(), markeredgewidth=0.75, markerfacecolor=getColor())
            # if labels: pl.text(x, y, label, fontsize="x-small")
        if labels:
            # pl.legend(scps, labels, loc=loc, scatterpoints=1, numpoints=1, fancybox=True) # passing scps & labels explicitly to work around a bug with legend seeming to miss out the 2nd scatterplot
            pl.legend(scps, labels, loc=(1.01, 0), scatterpoints=1, numpoints=1, fancybox=True)  # passing scps & labels explicitly to work around a bug with legend seeming to miss out the 2nd scatterplot
    pl.axis([-0.02, 1.02, -0.02, 1.02])  # xmin, xmax, ymin, ymax
    
    return pl
