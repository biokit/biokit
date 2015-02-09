#from biokit.viz.base import VizInput

import pylab
import pandas as pd
import numpy as np
#def hist2d(data, *args, **kargs):
#    h = Hist2d(data)
#    h.plot(*args, **kargs)

__all__ = ["Hist2d"]


class VizInput(object):
    def __init__(self, verbose=False):
        self.verbose = verbose


class Hist2d(VizInput):
    """data can be a dataframe with 2 columns or a numpy 2D array with 2 columns
    or 2 rows, or a list of arrays or a dictionary.


    """
    def __init__(self, data, verbose=False):
        super(Hist2d, self).__init__(verbose=verbose)
        self.df = pd.DataFrame(data)

        if self.df.shape[1] != 2:
            if self.df.shape[0] == 2:
                print("warning transposing data")
                self.df = self.df.transpose()

    def plot(self, bins=100, cmap="hot_r", fontsize=10, Nlevels=4,
        xlabel=None, ylabel=None, norm=None, range=None,
        contour=True, **kargs):
        """plots histogram of mean across replicates versus coefficient variation

        :param int bins: binning for the 2D histogram
        :param fontsize: fontsize for the labels
        :param contour: show some contours
        :param int Nlevels: must be more than 2
        :param range: as in pylab.hist2d : a 2x2 shape [[-3,3],[-4,4]]

        .. plot::
            :include-source:
            :width: 50%

            >>> from msdas import *
            >>> r = replicates.ReplicatesYeast(get_yeast_raw_data())
            >>> r.drop_na_count(54) # to speed up the plot creation
            >>> r.hist2d_mu_versus_cv()

        """

        X = self.df[self.df.columns[0]].values
        Y = self.df[self.df.columns[1]].values
        if len(X) > 10000:
            print("Computing 2D histogram. Please wait")

        pylab.clf()
        if norm == 'log':
            from matplotlib import colors
            res = pylab.hist2d(X, Y, bins=bins,
               cmap=cmap, norm=colors.LogNorm())
        else:
            res = pylab.hist2d(X, Y, bins=bins, cmap=cmap, range=range)

        pylab.colorbar()

        if contour:
            try:
                bins1 = bins[0]
                bins2 = bins[1]
            except:
                bins1 = bins
                bins2 = bins

            X, Y = pylab.meshgrid(res[1][0:bins1], res[2][0:bins2])
            if contour:
                levels = [round(x) for x in pylab.logspace(0, pylab.log10(res[0].max().max()),Nlevels)]
                pylab.contour(X, Y, res[0].transpose(), levels[2:], color="g")
                #pylab.clabel(C, fontsize=fontsize, inline=1)

        if ylabel == None:
            ylabel = self.df.columns[1]
        if xlabel == None:
            xlabel = self.df.columns[0]

        pylab.xlabel(xlabel, fontsize=fontsize)
        pylab.ylabel(ylabel, fontsize=fontsize)

        pylab.grid(True)
        return res


