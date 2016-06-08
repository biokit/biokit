import scipy.stats
import numpy as np
import pandas as pd



class ANOVA(object):
    """

    assumption: normality of the data and independence (eg. True across cell line,
        not over protein)
    """

    def __init__(self, df):

        self.df = df.copy()


    def anova(self):
        F, P = scipy.stats.f_oneway(*[self.df[x] for x in self.df.columns])
        return F, P


    def imshow_anova_pairs(self, log=True, **kargs):
        N = len(self.df.columns)

        # could use a dataframe straight way ?
        res = np.ones((N, N))
        for i,col1 in enumerate(self.df.columns):
            for j,col2 in enumerate(self.df.columns):
                d1 = self.df[col1]
                d2 = self.df[col2]
                F, P = scipy.stats.f_oneway(*[d1, d2])
                res[i][j] = P
        df = pd.DataFrame(res, index=self.df.columns, columns=self.df.columns)
        #FIXME: may have na, which are set to 1
        df = df.fillna(1)
        from biokit.viz import Imshow
        if log==True:  
            Imshow(-np.log10(df)).plot(**kargs)
        else:
            Imshow(df).plot(**kargs)
        return df

