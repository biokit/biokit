import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.patches import Ellipse, Circle, Rectangle, Wedge
import string

"""
references: http://cran.r-project.org/web/packages/corrplot/vignettes/corrplot-intro.html


todo:: 

 - addrect if clustering
 - colorbar

"""

class Corrplot(object):
    """

    Input must be a correlation matrix in pandas format with a square matrix and index and columns
    names identical. If not, we assume that the input data is not a a correlation matrix. A correlation is therefore computed in such case. 

    data could also be a correlation matrix, a 2-D numpy array containing
    the pairwise correlations between variables. 

    pvalues is a matrix containing the pvalue for each corresponding
    correlation value; if none it is assumed to be the zero matrix


    more options with the clustering/order + rectangle ?

    TODO

    values could be non-correlation between -100 and 100
    values could be confidence interval ??
    significance test: values above or below some threshold could be crossed or left blank (e.g. set to 0)
    """
    def __init__(self, data, pvalues=None):
        #input data can be a dataframe only
        self.df = data.copy()
        w, h = self.df.shape 
        
        
        if w !=h or list(self.df.index) != list(self.df.columns):
            try:
                print("Computing correlation")
                cor = self.df.corr()
                self.df = cor
                w, h = self.df.shape
            except:
                raise ValueError


        if pvalues is None:
            self.pvalues = np.zeros([w, h])
        else:
            self.values = values

        self.poscm = cm.get_cmap('Blues')
        self.negcm = cm.get_cmap('Oranges')
        self.negcm = cm.get_cmap('Reds')


    def order(self, method='complete', metric='euclidean',inplace=False):
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
        

    def plot(self, num=1, grid=True,
            rotation=30, colorbar_width=10, fill='both', lower=None, upper=None, 
            shrink=0.9, axisbg='white', colorbar=False, label_color='black',
            fontsize='small', edgecolor='black', method='ellipse', order=None):

        self.shrink = shrink
        self.fontsize = fontsize
        self.edgecolor = edgecolor

        if order == 'hclust':
            df = self.order(method='hclust')
        else:
            df = self.df

        plt.clf()
        fig = plt.figure(num=num, facecolor=axisbg)

        if colorbar:
            ax = plt.subplot(1, 2, 1, aspect='equal')
            axc = plt.subplot(1, 2, 2)
        else:
            ax = plt.subplot(1, 1, 1, aspect='equal', axisbg=axisbg)
        # subplot resets the bg color, let us set it again
        fig.set_facecolor(axisbg)


        width, height = df.shape
        labels = (df.columns)

        self.lower = lower
        self.upper = upper
        if self.lower is not None:
            self._fill_triangle(df, lower, 'lower',  ax)
        if self.upper is not None:
            self._fill_triangle(df, upper, 'upper', ax)
        if self.upper is None and self.lower is None:
            self._fill_triangle(df, method, fill,  ax)
        


        ax.set_xlim(-0.5, width-.5)
        ax.set_ylim(-0.5, height-.5)
            
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
                if fill == 'lower':
                    plt.axvline(i+.5, ymin=1-ratio1, ymax=0., color='grey')
                    plt.axhline(i+.5, xmin=0, xmax=ratio2, color='grey')
                elif fill == 'upper':
                    plt.axvline(i+.5, ymin=1 - ratio2, ymax=1, color='grey')
                    plt.axhline(i+.5, xmin=ratio1, xmax=1, color='grey')
                else:
                    plt.axvline(i+.5, color='grey')
                    plt.axhline(i+.5, color='grey')

            # can probably be simplified
            if fill == 'lower':
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
            elif fill == 'upper':
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
            from biokit.viz import imshow
            plt.sca(axc)
            imshow(np.transpose([np.linspace(-1,1,101)]*colorbar_width)) 
            plt.xticks([])
            plt.yticks([])

    def _fill_triangle(self, df, method, fill, ax):

        width, height = df.shape
        labels = (df.columns)

        for x in xrange(width):
            for y in xrange(height):

                if fill == 'lower':
                    if x>y:
                        continue
                elif fill == 'upper':
                    if x<y:
                        continue
                if self.lower and self.upper:
                    if x==y:
                        continue
                d = df.ix[x, y]
                c = self.pvalues[x, y]
                rotate = -45 if d > 0 else +45
                cmap = self.poscm if d >= 0 else self.negcm
                d_abs = np.abs(d)
                if method in ['ellipse', 'square', 'rectangle', 'color']:
                    if method == 'ellipse':
                        func = Ellipse
                        shape = func((x, y), width=1 * self.shrink,
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
                        shape = func((x + offset-.5, y + offset-.5), width=w,
                                  height=h, angle=0)
                    if self.edgecolor:
                        shape.set_edgecolor(self.edgecolor)
                    shape.set_facecolor(cmap(d_abs))
                    if c > 0.05:
                        shape.set_linestyle('dotted')
                    ax.add_artist(shape)
                    #FIXME edgecolor is always printed
                elif method=='circle':
                    circle = Circle((x, y), radius=d_abs*self.shrink/2.)
                    if self.edgecolor:
                        circle.set_edgecolor(self.edgecolor)
                    circle.set_facecolor(cmap(d_abs))
                    if c > 0.05:
                        circle.set_linestyle('dotted')
                    ax.add_artist(circle)
                elif method in ['number', 'text']:
                    from easydev import precision
                    #FIXME 
                    if d<0:
                        edgecolor = 'red'
                    elif d>0:
                        edgecolor = 'blue'
                    plt.text(x,y, precision(d, 2), color=edgecolor, 
                            fontsize=self.fontsize, horizontalalignment='center',
                            weight='bold', alpha=d_abs,
                            withdash=False)
                elif method == 'pie':
                    S = 360 * d_abs
                    patches = [
                        Wedge((x,y), 1*self.shrink/2., -90, S-90),       
                        Wedge((x,y), 1*self.shrink/2., S-90, 360-90),
                        ]
                    patches[0].set_facecolor(cmap(d_abs))
                    patches[1].set_facecolor('white')
                    if self.edgecolor:
                        patches[0].set_edgecolor(self.edgecolor)
                        patches[1].set_edgecolor(self.edgecolor)

                    ax.add_artist(patches[0])
                    ax.add_artist(patches[1])



if __name__ == "__main__":
    import pandas as pd
    df = pd.DataFrame(dict(( (k, np.random.random(10)) for k in ['ABCDEF'])))
    fig = Corrplot(df, None).plot()
    fig.show()

