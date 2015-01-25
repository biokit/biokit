import numpy as np
import pylab


__all__ = ['Volcano']


class Volcano(object):

    def __init__(self, X0, X1, pvalue=None, intensity=None):
        """data should be a time series/numpy array or whatever can be converted
        to 1D list. The data should be log2 fold change

        fold change depends on intensity (if you don't have a p-value), as there
        is more vairability at low intensities, so always keep an eye on the intensity
        as well as the fold change. Sort them by fold change, but have the average
        intensity on the side. A fold change of 3 but very low intensity is not very
        reliable...
        """


        self.fold_change = pylab.log2(X1 / X0)
        self.pvalue = pvalue
        if pvalue == None:
            # assume a normal distribution mean 0 and sigma 1
            import scipy.stats
            self.pvalue = - pylab.log10(scipy.stats.norm.pdf(abs(self.fold_change), 0,1)), 


        self.intensity = intensity
        if self.intensity is None:
            self.intensity = intensity

    def plot(self, size=100, alpha=0.5, fontsize=16):
        pylab.clf();
        pylab.scatter(self.fold_change, 
                self.pvalue,
#                -log10(scipy.stats.norm.pdf(abs(FC2), 0,1)), 
                s=size,
                alpha=alpha,
                c=self.intensity)
        pylab.grid()
        pylab.ylim([0, pylab.ylim()[1]])
        M = max(abs(self.fold_change)) * 1.1
        pylab.xlim([-M, M])
        pylab.xlabel('Fold Change', fontsize=fontsize)
        pylab.ylabel('p-value', fontsize=fontsize)


