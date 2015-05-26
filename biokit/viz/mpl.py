"""Imshow utility"""
from biokit.viz.core import VizInput2D
import pylab
import pandas as pd


__all__ = ['imshow', 'Imshow']


class Imshow(VizInput2D):
    def __init__(self, x, y=None, verbose=True):
        super(Imshow, self).__init__(x=x, y=y, verbose=verbose)

    
    def imshow(interpolation='None', aspect='auto', cmap='hot', tight_layout=True,
        colorbar=True, fontsize_x=None, fontsize_y=None, rotation_x=90,
        xticks_on=True, yticks_on=True, **kargs):
        """wrapper around imshow to plot a dataframe


        if list of lists or numpy array, no information about x and y axis will be filled
        otherwise, uses indedx and columns from the dataframe.
        """

        if isinstance(data, pd.DataFrame):
            pass
        else:
            # try a cast to df
            data = pd.DataFrame(data)

        pylab.clf()
        pylab.imshow(data, interpolation=interpolation, aspect=aspect, cmap=cmap, **kargs)

        if fontsize_x == None:
            fontsize_x = 16 #FIXME use default values
        if fontsize_y == None:
            fontsize_y = 16 #FIXME use default values

        if yticks_on is True:
            pylab.yticks(range(0, len(data.index)), data.index, 
                fontsize=fontsize_y)
        else:
            pylab.yticks([])
        if xticks_on is True:
            pylab.xticks(range(0, len(data.columns[:])), data.columns, 
                fontsize=fontsize_x, rotation=rotation_x)
        else:
            pylab.xticks([])

        if colorbar is True:
            pylab.colorbar()

        if tight_layout:
            pylab.tight_layout()





