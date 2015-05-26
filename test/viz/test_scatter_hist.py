


def test1():
    from biokit.viz import scatter_hist
    scatter_hist(x=[1,2,3,4], y=[3,5,6,4],
        kargs_scatter={
            's':[200,400,600,800],
            'c': ['red', 'green', 'blue', 'yellow'],
            'alpha':0.5},
        kargs_histx={'color': 'red'},
        kargs_histy={'color': 'green'})
