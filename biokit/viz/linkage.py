"""Heatmap and dendograms"""
import scipy.cluster.hierarchy as hierarchy
import scipy.spatial.distance as distance
import easydev


__all__ = ['Linkage']


class Linkage(object):
    """Linkage used in other tools such as Heatmap"""

    def __init__(self):
        """.. rubric:: constructor

        :param data: a dataframe or possibly a numpy matrix.

        """
        pass

    def check_metric(self, value):
        return
        from biokit.viz.commons import valid_metrics
        easydev.check_param_in_list(value, valid_metrics)

    def check_method(self, value):
        # None is possible
        # in R, in addition to single, complete, average, centroid, 
        # median and ward
        # there are  ward.D, wardD2 and mcquitty
        # default is complete
        return
        from biokit.viz.commons import valid_methods
        easydev.check_param_in_list(str(value), valid_methods)

    def linkage(self, df, method, metric):
        self.check_metric(metric)
        self.check_method(method)
        d = distance.pdist(df)
        D = distance.squareform(d)
        Y = hierarchy.linkage(D, method=method, metric=metric)
        return Y
