from biokit.viz.extra import scatter_hist



def test_scatter_hist():
    import pylab
    X = pylab.randn(1000)
    Y = pylab.randn(1000)
    scatter_hist(X, Y)

