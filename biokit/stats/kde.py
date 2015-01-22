import pylab

from scipy.stats import gaussian_kde





class KDE(object):

    def __init__(self, data):
        self.data = data

    def hist(self, bins, **kwargs):
        pylab.hist(self.data, bins=bins, **kwargs)

    def kde_scipy(self, x_grid, bandwidth=0.2, **kwargs):
        """Kernel Density Estimation with Scipy"""
        # Note that scipy weights its bandwidth by the covariance of
        # the input data.  To make the results comparable to the
        # other methods, we divide the bandwidth by the sample
        # standard deviation here.
        kde = gaussian_kde(self.data,  bw_method=bandwidth /
                  self.std(ddof=1), **kwargs)
        return kde.evaluate(x_grid)

    def kde_statsmodels_u(self, x_grid, bandwidth=0.2, **kwargs):
        """Univariate Kernel Density Estimation with Statsmodels"""
        from statsmodels.nonparametric.kde import KDEUnivariate
        kde = KDEUnivariate(self.data)
        kde.fit(bw=bandwidth, **kwargs)
        return kde.evaluate(x_grid)
                
    def kde_statsmodels_m(self, x_grid, bandwidth=0.2, **kwargs):
        """Multivariate Kernel Density Estimation with
        Statsmodels"""
        from statsmodels.nonparametric.kernel_density import KDEMultivariate
        kde = KDEMultivariate(self.data, bw=bandwidth * np.ones_like(x), var_type='c', **kwargs)
        return kde.pdf(x_grid)

    def kde_sklearn(self, x_grid, bandwidth=0.2, **kwargs):
        """Kernel Density Estimation with
        Scikit-learn"""
        from sklearn.neighbors import KernelDensity
        kde_skl = KernelDensity(bandwidth=bandwidth,**kwargs)
        kde_skl.fit(self.data[:, np.newaxis])
        # score_samples() returns the
        # log-likelihood of the samples
        log_pdf = kde_skl.score_samples(x_grid[:, np.newaxis])
        return np.exp(log_pdf)
