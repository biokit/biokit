from biokit.viz import corrplot
import string
import pandas as pd
import numpy as np



class TestCorrplot(object):

    @classmethod
    def setup_class(klass):
        letters = string.uppercase[0:10]
        df = pd.DataFrame(dict(( (k, np.random.random(10)+ord(k)-65) for k in letters)))
        klass.s = corrplot.Corrplot(df.corr())
        klass.s = corrplot.Corrplot(df)

    def test_plot_square(self):
        self.s.plot(colorbar=False, method='square', shrink=.9, rotation=45)

    def test_plot_text(self):
        self.s.plot(method='text', fontsize=8)

    def test_plot_color(self):
        self.s.plot(method='color')


    def test_(self):
        self.s.plot(method='pie', shrink=.8)


    def test_lower(self):
        self.s.plot(colorbar=False, method='circle', shrink=.9, lower='circle'  )

    def test_upper(self):
        self.s.plot(colorbar=False, method='circle', shrink=.9, upper='circle'  )

