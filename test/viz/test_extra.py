from biokit.viz.extra import scatter_hist
import pandas as pd


def test_scatter_hist():
    import pylab
    X = pylab.randn(1000)
    Y = pylab.randn(1000)
    scatter_hist(X, Y)


    df = pd.DataFrame({'X':X, 'Y':Y, 'size':X, 'color':Y})
    scatter_hist(df, hist_position='left')

    df = pd.DataFrame({'X':X})
    try:
        scatter_hist(df, hist_position='left')
        assert False
    except:
        assert True
