"""

Corrplot example
==================

"""
# some useful pylab imports for this notebook


# Create some random data
import string
letters = string.ascii_uppercase[0:15]
import pandas as pd
import numpy as np
df = pd.DataFrame(dict(( (k, np.random.random(10)+ord(k)-65) for k in letters)))
df = df.corr()

# if the input is not a square matrix or indices do not match 
# column names, correlation is computed on the fly
from biokit.viz import corrplot
c = corrplot.Corrplot(df)


c.plot(colorbar=False, method='square', shrink=.9 ,rotation=45)


