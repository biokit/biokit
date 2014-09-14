import pylab


__all__ = ['imshow']

def imshow(data, interpolation='None', cmap='hot', tight_layout=True,
        colorbar=True, fontsize_x=None, fontsize_y=None, **kargs):
    """wrapper around imshow to plot a dataframe


    """
    pylab.clf()
    pylab.imshow(data, interpolation=interpolation, cmap=cmap, **kargs)

    if fontsize_x == None:
        fontsize_x = 16 #FIXME use default values
    if fontsize_y == None:
        fontsize_y = 16 #FIXME use default values
    pylab.yticks(range(0, len(data.index)), data.index, 
            fontsize=fontsize_x)
    pylab.xticks(range(0, len(data.columns[:])), data.columns, 
            fontsize=fontsize_y, rotation=90)

    if colorbar is True:
        pylab.colorbar()

    if tight_layout:
        pylab.tight_layout()



def heatmap(df):
    raise NotImplementedError


