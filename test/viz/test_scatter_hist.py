


def test1():
    from biokit.viz import scatter_hist
    scatter_hist(x=[1,2,3,4], y=[3,5,6,4],
        kargs_scatter={
            's':[200,400,600,800],
            'c': ['red', 'green', 'blue', 'yellow'],
            'alpha':0.5},
        kargs_histx={'color': 'red'},
        kargs_histy={'color': 'green'})

    from biokit.viz import ScatterHist

    s = ScatterHist(x=[1,2,3,4], y=[3,4,5,6])
    s.plot()
    s.plot(scatter_position='top right')
    s.plot(scatter_position='top left')
    s.plot(scatter_position='bottom right')
