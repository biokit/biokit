"""

Hist2d using Pandas dataframe as input
==========================================


"""



#################################################"
# wrapping of pylab hist2d function.
import pylab

from biokit import viz

X = pylab.randn(10000)
Y = pylab.randn(10000)


import pandas as pd
df = pd.DataFrame({'X':X, 'Y':Y})


from biokit.viz import hist2d
h = hist2d.Hist2D(df)
res = h.plot(bins=[40,40], contour=True, nnorm='log', Nlevels=6)


