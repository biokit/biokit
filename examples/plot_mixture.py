"""

Gaussian Mixture model
=========================

Fit a Gaussian Mixture Models (2 distributions) using brute force optimisation method.

"""

from biokit.stats.mixture import GaussianMixture, GaussianMixtureFitting
m = GaussianMixture(mu=[-1,1], sigma=[0.5,0.5], mixture=[0.2,0.8])
mf = GaussianMixtureFitting(m.data)
mf.estimate(k=2)
mf.plot()

