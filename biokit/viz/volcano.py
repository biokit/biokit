"""Volcano plot"""

import numpy as np
import pylab


__all__ = ['Volcano']


class Volcano(object):
    """Volcano plot

    In essence, just a scatter plot with annotations.

    .. todo:: color on each dot 
    .. todo:: use dataframe with fold change, color, alpha, pvalue as columnns


    .. plot::
        :width: 80%
        :include-source: 

        import numpy as np
        fc = np.random.randn(1000)
        pvalue = np.random.randn(1000)

        from biokit import Volcano
        v = Volcano(fc, -np.log10(pvalue**2))
        v.plot(pvalue_threshold=3)


    """

    def __init__(self, fold_changes=None, pvalues=None):
        """.. rubric:: constructor
        
        
        :param list fold_changes: 1D array or list 
        :param list pvalues: 1D array or list


        """
        # try to compute the FC now 
        #if self.fold_change is None:
        #    self.fold_change = pylab.log2(X1/X0)

        #if pvalue is None:
        #    # assume a normal distribution mean 0 and sigma 1
        #    import scipy.stats
        #    self.pvalue = - pylab.log10(scipy.stats.norm.pdf(abs(self.fold_change), 0,1)), 

        self.fold_changes = np.array(fold_changes)
        self.pvalues = np.array(pvalues)

    def plot(self, size=100, alpha=0.5, marker='o', fontsize=16, xlabel='log2 fold change',
            ylabel='-log10 p-value', pvalue_threshold=1.5, fold_change_threshold=1):
        """

        :param size: size of the markers
        :param alpha: transparency of the marker
        :param fontsize: 
        :param xlabel:
        :param ylabel:
        :param pvalue_threshold: adds an horizontal dashed line at
           the threshold provided.
        :param fold_change_threshold: colors in grey the absolute fold 
            changes below a given threshold.


        """
        pylab.clf()
        mask1 = abs(self.fold_changes) < fold_change_threshold
        mask2 = abs(self.fold_changes) >= fold_change_threshold

        pylab.scatter(self.fold_changes[mask1], 
                self.pvalues[mask1],
                s=size,
                alpha=alpha,
                c='grey', marker=marker)
        pylab.scatter(self.fold_changes[mask2], 
                self.pvalues[mask2],
                s=size,
                alpha=alpha,
                c='blue')

        pylab.grid()
        #pylab.ylim([0, pylab.ylim()[1]])
        #M = max(abs(self.fold_change)) * 1.1
        #pylab.xlim([-M, M])
        pylab.xlabel(xlabel, fontsize=fontsize)
        pylab.ylabel(ylabel, fontsize=fontsize)
        pylab.axhline(pvalue_threshold, color='red', linestyle='--')



