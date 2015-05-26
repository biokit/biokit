from pylab import scatter, hist, axes, clf
import pylab


__all__ = ["scatter_hist"]


def scatter_hist(x, y=None, 
        kargs_scatter={'s':20, 'c':'b'}, 
        kargs_grids={},
        kargs_histx={},
        kargs_histy={},
        hist_position='right',
        width=.5,
        height=.5,
        offset_x=.10,
        offset_y=.10,
        gap=0.06,
        grid=True,
        **kargs):
    """data could be numpy array or list of lists of dataframe

    if x and y provided, assume a 2D data set with X and Y ->> scatter
    if X only -> imshow from array or pandas

    other kargs are: hold
    histx_position can be 'top'/'bottom'
    histy_position can be 'left'/'right'

    .. plot::
        :include-source:
        :width: 50%

        from biokit.viz import scatter_hist
        import pylab
        import pandas as pd
        X = pylab.randn(1000)
        Y = pylab.randn(1000)
        df = pd.DataFrame({'X':X, 'Y':Y})
        scatter_hist(df)


    .. seealso:: `notebook <http://nbviewer.ipython.org/github/biokit/biokit/blob/master/notebooks/viz/biokit.viz examples.ipynb>`_
    """
    # if 2D --> scatter ->
    # if pandas matrix -> imshow + mean or sum 
    if y is None:
        try: # is it a pandas df ?
            y = x.ix[:,1].values # first let us fill y and
            try:
                size = x['size']
                kargs_scatter['s'] = size
            except:
                pass
            try:
                color = x['color']
                kargs_scatter['c'] = color
            except:
                pass
            x = x.ix[:,0].values # second overwrite x

        except Exception as err:
            raise(err)

    if kargs.get("hold", False) is False:
        pylab.clf()

    W = width
    H = height
    if hist_position == 'right':
        X0 = offset_x
        Y0 = offset_y
        Xoff = X0 + W + gap
        Yoff = Y0 + H + gap
        Wh = 1 - offset_x*2 - W - gap
        Hh = 1 - offset_y*2 - H - gap
    elif hist_position == 'left':
        Wh = 1 - offset_x*2 - W - gap
        Hh = 1 - offset_y*2 - H - gap
        X0 = offset_x + Wh +gap
        Y0 = offset_y
        Xoff = offset_x
        Yoff = Y0 + H + gap

    axisbg = kargs.get('axisbg', 'white')

    ax_scatter = axes((X0, Y0, W, H), axisbg=axisbg, xscale='linear', 
            yscale='linear')#, xticks='auto', yticks='auto')
    ax_hist_x = axes((X0, Yoff, W, Hh), axisbg=axisbg, xscale='linear', 
            yscale='linear')#, xticks='auto', yticks='auto')
    ax_hist_y = axes((Xoff, Y0, Wh, H), axisbg=axisbg, xscale='linear', 
            yscale='linear')#, xticks='auto', yticks='auto')

    # move ticks on axis  if needed
    ax_hist_x.xaxis.set_ticks_position('top')
    if hist_position == 'left':
        ax_scatter.yaxis.set_ticks_position('right')
        ax_hist_x.yaxis.set_ticks_position('right')
    elif hist_position == 'right':
        ax_hist_y.yaxis.set_ticks_position('right')


    ax_scatter.scatter(x,y, **kargs_scatter)
    ax_hist_x.hist(x, **kargs_histx)
    # fixme: user may not want that ?
    kargs_histy['orientation'] = 'horizontal'
    ax_hist_y.hist(y, **kargs_histy)
    # I tried c.set_xticks but rotation could not be found
    pylab.xticks(ax_hist_y.get_xticks(), rotation=90)

    # grid?
    ax_scatter.grid(b=grid, which='major', axis='both', **kargs_grids)
    ax_hist_x.grid(b=grid, which='major', axis='both', **kargs_grids)
    ax_hist_y.grid(b=grid, which='major', axis='both', **kargs_grids)

    return (ax_scatter, ax_hist_x, ax_hist_y)



