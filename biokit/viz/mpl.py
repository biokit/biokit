import pylab
import pandas as pd

__all__ = ['imshow']


def imshow(data, interpolation='None', cmap='hot', tight_layout=True,
        colorbar=True, fontsize_x=None, fontsize_y=None, rotation_x=90, **kargs):
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
    pylab.imshow(data, interpolation=interpolation, cmap=cmap, **kargs)

    if fontsize_x == None:
        fontsize_x = 16 #FIXME use default values
    if fontsize_y == None:
        fontsize_y = 16 #FIXME use default values
    pylab.yticks(range(0, len(data.index)), data.index, 
            fontsize=fontsize_y)
    pylab.xticks(range(0, len(data.columns[:])), data.columns, 
            fontsize=fontsize_x, rotation=rotation_x)

    if colorbar is True:
        pylab.colorbar()

    if tight_layout:
        pylab.tight_layout()





