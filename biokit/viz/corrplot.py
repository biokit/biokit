import string

from colormap import cmap_builder

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Ellipse, Circle, Rectangle, Wedge
from matplotlib.collections import PatchCollection
import pandas as pd
"""

references: http://cran.r-project.org/web/packages/corrplot/vignettes/corrplot-intro.html


todo::

 - addrect if clustering

"""

class Corrplot(object):
    """An implementation of correlation plotting tools (corrplot)

    Input must be a dataframe (Pandas) with data (any values) or a correlation
    matrix (square) with values between -1 and 1.

    If NAs are found in the correlation matrix, there are replaced with zeros.

    Data can also be a correlation matrix as a 2-D numpy array containing
    the pairwise correlations between variables. Labels will be numerical
    indices though.

    By default from red for positive correlation to blue for negative ones but
    other colormaps can easily be provided.

    .. plot::
        :width: 50%
        :include-source:

        from biokit.viz import corrplot
        import string
        letters = string.uppercase[0:10]
        import pandas as pd
        df = pd.DataFrame(dict(( (k, np.random.random(10)+ord(k)-65) for k in letters)))

        c = corrplot.Corrplot(df)
        c.plot()

    .. seealso::    All functionalities are covered in this 
        `notebook <http://nbviewer.ipython.org/github/biokit/biokit/blob/master/notebooks/viz/corrplot.ipynb>`_

    """
    def __init__(self, data, pvalues=None, na=0):
        #input data can be a dataframe only
        #try:
        self.df = pd.DataFrame(data, copy=True)
        #except:
        #    self.df = pd.DataFrame(data)

        compute_correlation = False
        w, h = self.df.shape
        if self.df.max().max() >1 or self.df.min().min()<-1:
            compute_correlation = True
        if w !=h:
            compute_correlation = True
        if list(self.df.index) != list(self.df.columns):
            compute_correlation = True

        if compute_correlation:
            print("Computing correlation")
            cor = self.df.corr()
            self.df = cor

        # replace NA with zero
        self.df.fillna(na, inplace=True)

        self.params = {'colorbar.N': 100, 'colorbar.orientation':'vertical'}



    def _set_default_cmap(self):
        self.cm = cmap_builder('#AA0000','white','darkblue')

    def order(self, method='complete', metric='euclidean',inplace=False):
        """Rearrange the order of rows and columns after clustering

        :param method: any scipy method
        :param metric: any scipy distance
        :param bool inplace: if set to True, the dataframe is replaced

        """
        import scipy.cluster.hierarchy as hierarchy
        import scipy.spatial.distance as distance
        d = distance.pdist(self.df)
        D = distance.squareform(d)
        Y = hierarchy.linkage(D, method=method, metric=metric)
        ind1 = hierarchy.fcluster(Y, 0.7*max(Y[:,2]), 'distance')
        Z = hierarchy.dendrogram(Y, no_plot=True)
        idx1 = Z['leaves']
        cor2 = self.df.ix[idx1][idx1]
        if inplace is True:
            self.df = cor2
        else:
            return cor2
        self.Y = Y
        self.Z = Z
        self.idx1 = idx1
        self.ind1 = ind1

        #treee$order == Z.leaves and c.idx1
        # hc = c.ind1

        #clustab <- table(hc)[unique(hc[tree$order])]
        #cu <- c(0, cumsum(clustab))
        #mat <- cbind(cu[-(k + 1)] + 0.5, n - cu[-(k + 1)] + 0.5,
        #cu[-1] + 0.5, n - cu[-1] + 0.5)
        #rect(mat[,1], mat[,2], mat[,3], mat[,4], border = col, lwd = lwd)

    def plot(self, num=1, grid=True,
            rotation=30, colorbar_width=10, lower=None, upper=None,
            shrink=0.9, axisbg='white', colorbar=True, label_color='black',
            fontsize='small', edgecolor='black', method='ellipse', order=None,
            cmap=None
            ):
        """plot the correlation matrix from the content of :attr:`df`
        (dataframe)

        :param grid: add grid (Defaults to True)
        :param rotation: rotate labels on y-axis
        :param lower: if set to a valid method, plots the data on the lower
            left triangle
        :param upper: if set to a valid method, plots the data on the upper
            left triangle
        :param method: shape to be used in 'ellipse', 'square', 'rectangle', 
            'color', 'text', 'circle',  'number', 'pie'.
        :param cmap: a valid cmap from matplotlib of colormap package (e.g.,
        jet, or 

        Here are some examples provided that the data is created and pass to c::

            c = corrplot.Corrplor(dataframe)
            c.plot(cmap=('Orange', 'white', 'green'))
            c.plot(method='circle')
            c.plot(colorbar=False, shrink=.8, upper='circle'  )


        """

        # default
        if cmap != None:
            try:
                if isinstance(cmap, str):
                    self.cm = cmap_builder(cmap)
                else:
                    self.cm = cmap_builder(*cmap)
            except:
                print("incorrect cmap. Use default one")
                self._set_default_cmap()
        else:
            self._set_default_cmap()

        self.shrink = shrink
        self.fontsize = fontsize
        self.edgecolor = edgecolor

        if order == 'hclust':
            df = self.order(method='hclust')
        else:
            df = self.df

        plt.clf()
        fig = plt.figure(num=num, facecolor=axisbg)

        ax = plt.subplot(1, 1, 1, aspect='equal', axisbg=axisbg)
        # subplot resets the bg color, let us set it again
        fig.set_facecolor(axisbg)

        width, height = df.shape
        labels = (df.columns)

        # add all patches to the figure
        # TODO check value of lower and upper

        if upper is None and lower is None:
            mode = 'method'
            diagonal = True
        elif upper and lower:
            mode = 'both'
            diagonal = False
        elif lower is not None:
            mode = 'lower'
            diagonal = True
        elif upper is not None:
            mode = 'upper'
            diagonal = True
        else:
            raise ValueError

        if mode == 'upper':
            self._add_patches(df, upper, 'upper',  ax, diagonal=True)
        elif mode == 'lower':
            self._add_patches(df, lower, 'lower',  ax, diagonal=True)
        elif mode == 'method':
            self._add_patches(df, method, 'both',  ax, diagonal=True)
        elif mode == 'both':
            self._add_patches(df, upper, 'upper',  ax, diagonal=False)
            self._add_patches(df, lower, 'lower',  ax, diagonal=False)

        # shift the limits to englobe the patches correctly
        ax.set_xlim(-0.5, width-.5)
        ax.set_ylim(-0.5, height-.5)

        # set xticks/xlabels on top
        ax.xaxis.tick_top()
        xtickslocs = np.arange(len(labels))
        ax.set_xticks(xtickslocs)
        ax.set_xticklabels(labels, rotation=rotation, color=label_color,
                fontsize=fontsize, ha='left')

        ax.invert_yaxis()
        ytickslocs = np.arange(len(labels))
        ax.set_yticks(ytickslocs)
        ax.set_yticklabels(labels, fontsize=fontsize, color=label_color)
        plt.tight_layout()

        if grid is True:
            for i in range(0, width):
                ratio1 = float(i)/width
                ratio2 = float(i+2)/width
                # TODO 1- set axis off
                # 2 - set xlabels along the diagonal
                # set colorbar either on left or bottom
                if mode == 'lower':
                    plt.axvline(i+.5, ymin=1-ratio1, ymax=0., color='grey')
                    plt.axhline(i+.5, xmin=0, xmax=ratio2, color='grey')
                if mode == 'upper':
                    plt.axvline(i+.5, ymin=1 - ratio2, ymax=1, color='grey')
                    plt.axhline(i+.5, xmin=ratio1, xmax=1, color='grey')
                if mode in ['method', 'both']:
                    plt.axvline(i+.5, color='grey')
                    plt.axhline(i+.5, color='grey')

            # can probably be simplified
            if mode == 'lower':
                plt.axvline(-.5, ymin=0, ymax=1, color='grey')
                plt.axvline(width-.5, ymin=0, ymax=1./width, color='grey', lw=2)
                plt.axhline(width-.5, xmin=0, xmax=1, color='grey',lw=2)
                plt.axhline(-.5, xmin=0, xmax=1./width, color='grey',lw=2)
                plt.xticks([])
                for i in range(0, width):
                    plt.text(i, i-.6 ,labels[i],fontsize=fontsize,
                            color=label_color,
                            rotation=rotation, verticalalignment='bottom')
                    plt.text(-.6, i ,labels[i],fontsize=fontsize,
                            color=label_color,
                            rotation=0, horizontalalignment='right')
                plt.axis('off')
            # can probably be simplified
            elif mode == 'upper':
                plt.axvline(width-.5, ymin=0, ymax=1, color='grey', lw=2)
                plt.axvline(-.5, ymin=1-1./width, ymax=1, color='grey', lw=2)
                plt.axhline(-.5, xmin=0, xmax=1, color='grey',lw=2)
                plt.axhline(width-.5, xmin=1-1./width, xmax=1, color='grey',lw=2)
                plt.yticks([])
                for i in range(0, width):
                    plt.text(-.6+i, i ,labels[i],fontsize=fontsize,
                            color=label_color, horizontalalignment='right',
                            rotation=0)
                    plt.text(i, -.5 ,labels[i],fontsize=fontsize,
                            color=label_color, rotation=rotation, verticalalignment='bottom')
                plt.axis('off')

        # set all ticks length to zero
        ax = plt.gca()
        ax.tick_params(axis='both',which='both', length=0)

        if colorbar:
            N = self.params['colorbar.N']
            cb = plt.gcf().colorbar(self.collection,
                    orientation=self.params['colorbar.orientation'], shrink=.9,
                boundaries= np.linspace(0,1,N), ticks=[0,.25, 0.5, 0.75,1])
            cb.ax.set_yticklabels([-1,-.5,0,.5,1])
            cb.set_clim(0,1) # make sure it goes from -1 to 1 even though actual values may not reach that range

    def _add_patches(self, df, method, fill, ax, diagonal=True):
        width, height = df.shape
        labels = (df.columns)

        patches = []
        colors = []
        for x in range(width):
            for y in range(height):
                if fill == 'lower' and x > y:
                    continue
                elif fill == 'upper' and x < y:
                    continue
                if diagonal is False and x==y:
                    continue
                datum = (df.ix[x, y] +1.)/2.
                d = df.ix[x, y]
                d_abs = np.abs(d)
                #c = self.pvalues[x, y]
                rotate = -45 if d > 0 else +45
                #cmap = self.poscm if d >= 0 else self.negcm
                if method in ['ellipse', 'square', 'rectangle', 'color']:
                    if method == 'ellipse':
                        func = Ellipse
                        patch = func((x, y), width=1 * self.shrink,
                                  height=(self.shrink - d_abs*self.shrink), angle=rotate)
                    else:
                        func = Rectangle
                        w = h = d_abs * self.shrink
                        #FIXME shring must be <=1
                        offset = (1-w)/2.
                        if method == 'color':
                            w = 1
                            h = 1
                            offset = 0
                        patch = func((x + offset-.5, y + offset-.5), width=w,
                                  height=h, angle=0)
                    if self.edgecolor:
                        patch.set_edgecolor(self.edgecolor)
                    #patch.set_facecolor(cmap(d_abs))
                    colors.append(datum)
                    if d_abs > 0.05:
                        patch.set_linestyle('dotted')
                    #ax.add_artist(patch)
                    patches.append(patch)
                    #FIXME edgecolor is always printed
                elif method=='circle':
                    patch = Circle((x, y), radius=d_abs*self.shrink/2.)
                    if self.edgecolor:
                        patch.set_edgecolor(self.edgecolor)
                    #patch.set_facecolor(cmap(d_abs))
                    colors.append(datum)
                    if d_abs > 0.05:
                        patch.set_linestyle('dotted')
                    #ax.add_artist(patch)
                    patches.append(patch)
                elif method in ['number', 'text']:
                    if d<0:
                        edgecolor = self.cm(-1.0)
                    elif d>=0:
                        edgecolor = self.cm(1.0)
                    d_str = "{:.2f}".format(d).replace("0.", ".").replace(".00", "")
                    ax.text(x,y, d_str, color=edgecolor,
                            fontsize=self.fontsize, horizontalalignment='center',
                            weight='bold', alpha=max(0.5, d_abs), 
                            withdash=False)
                elif method == 'pie':
                    S = 360 * d_abs
                    patch = [
                        Wedge((x,y), 1*self.shrink/2., -90, S-90),
                        Wedge((x,y), 1*self.shrink/2., S-90, 360-90),
                        ]
                    #patch[0].set_facecolor(cmap(d_abs))
                    #patch[1].set_facecolor('white')
                    colors.append(datum)
                    colors.append(0.5)
                    if self.edgecolor:
                        patch[0].set_edgecolor(self.edgecolor)
                        patch[1].set_edgecolor(self.edgecolor)

                    #ax.add_artist(patch[0])
                    #ax.add_artist(patch[1])
                    patches.append(patch[0])                    
                    patches.append(patch[1])
        if len(patches):                    
            col1 = PatchCollection(patches, array=np.array(colors), cmap=self.cm)
            ax.add_collection(col1)

            self.collection = col1


if __name__ == "__main__":
    import pandas as pd
    df = pd.DataFrame(dict(( (k, np.random.random(10)) for k in ['ABCDEF'])))
    fig = Corrplot(df, None).plot()
    fig.show()
