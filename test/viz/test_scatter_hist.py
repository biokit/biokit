


def test1():
    from biokit.viz import ScatterHist

    s = ScatterHist(x=[1,2,3,4], y=[3,4,5,6])
    s.plot()
    s.plot(scatter_position='top right')
    s.plot(scatter_position='top left')
    s.plot(scatter_position='bottom right')
