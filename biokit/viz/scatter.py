""".. rubric:: Scatter plots

:author: Thomas Cokelaer
"""
from pylab import scatter, hist, axes, clf
import pylab
import pandas as pd

__all__ = ["scatter_hist"]


def scatter_hist(x, y=None, 
        kargs_scatter={'s':20, 'c':'b'}, 
        kargs_grids={},
        kargs_histx={},
        kargs_histy={},
        scatter_position='bottom left',
        width=.5,
        height=.5,
        offset_x=.10,
        offset_y=.10,
        gap=0.06,
        axisbg='lightgrey',
        grid=True,
        **kargs):
    """Scatter plot of set of 2 vectors and their histograms.
    
    :param x: a dataframe or a numpy matrix (2 vectors) or a list of 2 items, 
        which can be a mix of list or numpy array.
        if **size** and/or **color** are found in the columns dataframe, 
        those columns will be used in the scatter plot. kargs_scatter keys **c**
        and **s** will then be ignored. If a list of lists, **x** will be the first row
        and **y** the second row.
    :param y: if x is a list or an array, then y must also be provided as 
        a list or an array
    :param kargs_scatter: a dictionary with pairs of key/value accepted by 
        matplotlib.scatter function. Examples is a list of colors or a list
        of sizes as shown in the examples below. 
    :param kargs_grid: a dictionary with pairs of key/value accepted by
        the maplotlib.grid (applied on histogram and axis at the same time)
    :param kargs_histx: a dictionary with pairs of key/value accepted by the
        matplotlib.histogram
    :param kargs_histy: a dictionary with pairs of key/value accepted by the
        matplotlib.histogram
    :param kargs: other optional parameters are **hold**, **axisbg**.
    :param scatter_position: can be 'bottom right/bottom left/top left/top right'
    :param width: width of the scatter plot (value between 0 and 1)
    :param height: height of the scatter plot (value between 0 and 1)
    :param offset_x:
    :param offset_y:
    :param gap: gap between the scatter and histogram plots.
    :param grid: defaults to True

    :return: the scatter, histogram1 and histogram2 axes.

    .. plot::
        :include-source:
        :width: 50%

        import pylab
        import pandas as pd
        X = pylab.randn(1000)
        Y = pylab.randn(1000)
        df = pd.DataFrame({'X':X, 'Y':Y})

        from biokit.viz import scatter_hist
        scatter_hist(df)


    .. plot::
        :include-source:
        :width: 50%

        from biokit.viz import scatter_hist
        scatter_hist(x=[1,2,3,4], y=[3,5,6,4], 
            kargs_scatter={
                's':[200,400,600,800], 
                'c': ['red', 'green', 'blue', 'yellow'], 
                'alpha':0.5},
            kargs_histx={'color': 'red'},
            kargs_histy={'color': 'green'})


    .. seealso:: `notebook <http://nbviewer.ipython.org/github/biokit/biokit/blob/master/notebooks/viz/biokit.viz examples.ipynb>`_
    """
    # input can be a dataframe, or something that will provide a dataframe with at least 2 input columns
    # as X, Y. additional columns if named as size, color will be used.
    # So, it could be a dictionary, a list of lists or a 


    if y is None:
        # if y is not provided, x can be a data compatible
        # with the dataframe instance that is a dataframe itself, 
        # a list of 2 items, which can be lists or numpy arrays.
        if isinstance(x, pd.DataFrame) is True:
            df = x.copy()
            columns = list(df.columns)
            columns[0] = 'x'
            columns[1] = 'y'
            df.columns = columns
        else:
            df = pd.DataFrame({'x':x[0], 'y':x[1]})

        try:
            kargs_scatter['s'] = df['size']
        except:
            pass
        try:
            kargs_scatter['c'] = df['color']
        except:
            pass
    else:
        df = pd.DataFrame({'x':x, 'y':y})

    if kargs.get("hold", False) is False:
        pylab.clf()

    W = width
    H = height
    if scatter_position == 'bottom left':
        X0 = offset_x
        Y0 = offset_y
        Xoff = X0 + W + gap
        Yoff = Y0 + H + gap
        Wh = 1 - offset_x*2 - W - gap
        Hh = 1 - offset_y*2 - H - gap
    elif scatter_position == 'bottom right':
        Wh = 1 - offset_x*2 - W - gap
        Hh = 1 - offset_y*2 - H - gap
        X0 = offset_x + Wh +gap
        Y0 = offset_y
        Xoff = offset_x
        Yoff = Y0 + H + gap
    elif scatter_position == 'top right':
        Wh = 1 - offset_x*2 - W - gap
        Hh = 1 - offset_y*2 - H - gap
        X0 = offset_x + Wh +gap
        Y0 = offset_y + Hh + gap 
        Xoff = offset_x
        Yoff = offset_y
    elif scatter_position == 'top left':
        Wh = 1 - offset_x*2 - W - gap
        Hh = 1 - offset_y*2 - H - gap
        X0 = offset_x 
        Y0 = offset_y + Hh + gap
        Xoff = offset_x + W + gap
        Yoff = offset_y #Y0 #+ H + gap
    else:
        raise ValueError("scatter_position must be 'top left', 'top right', 'bottom left', 'bottom right'")
        
    axisbg = kargs.get('axisbg', 'lightgrey')

    ax_scatter = axes((X0, Y0, W, H), axisbg=axisbg, xscale='linear', 
            yscale='linear')#, xticks='auto', yticks='auto')
    ax_hist_x = axes((X0, Yoff, W, Hh), axisbg=axisbg, xscale='linear', 
            yscale='linear')#, xticks='auto', yticks='auto')
    ax_hist_y = axes((Xoff, Y0, Wh, H), axisbg=axisbg, xscale='linear', 
            yscale='linear')#, xticks='auto', yticks='auto')

    # move ticks on axis  if needed
    ax_hist_x.xaxis.set_ticks_position('top')
    if scatter_position == 'bottom left':
        ax_scatter.yaxis.set_ticks_position('left')
        ax_hist_x.yaxis.set_ticks_position('right')
    elif scatter_position == 'bottom right':
        ax_hist_y.yaxis.set_ticks_position('left')
    elif scatter_position == 'top right':
        ax_scatter.xaxis.set_ticks_position('top')
        ax_scatter.yaxis.set_ticks_position('right')
        ax_hist_y.yaxis.set_ticks_position('left')
        ax_hist_x.xaxis.set_ticks_position('bottom')
    elif scatter_position == 'top left':
        ax_scatter.xaxis.set_ticks_position('top')
        ax_hist_y.yaxis.set_ticks_position('right')
        ax_hist_x.xaxis.set_ticks_position('bottom')
    else:
        raise ValueError("scatter_position must be 'top left', 'top right', 'bottom left', 'bottom right'")

    ax_scatter.scatter(df.x, df.y, **kargs_scatter)
    ax_hist_x.hist(df.x, **kargs_histx)
    # fixme: user may not want that ?
    kargs_histy['orientation'] = 'horizontal'
    ax_hist_y.hist(df.y, **kargs_histy)
    # I tried c.set_xticks but rotation could not be found
    pylab.xticks(ax_hist_y.get_xticks(), rotation=90)

    # grid
    if grid is True:
        ax_scatter.grid(b=grid, which='major', axis='both', **kargs_grids)
        ax_hist_x.grid(b=grid, which='major', axis='both', **kargs_grids)
        ax_hist_y.grid(b=grid, which='major', axis='both', **kargs_grids)

    return (ax_scatter, ax_hist_x, ax_hist_y)



