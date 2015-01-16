# source
# http://nbviewer.ipython.org/github/tritemio/notebooks/blob/master/Mixture_Model_Fitting.ipynb

from easydev import DevTools
devtools = DevTools()
from scipy.optimize import minimize, show_options
import numpy as np
import pylab
import seaborn as sns

class Mixture(object):
    """Creates a mix of Gaussian distribution


    """
    def __init__(self, mu=[-1,1], sigma=[1,1], mixture=[0.5,0.5], N=1000):
        assert len(mu) == len(sigma)
        assert len(mu) == len(mixture)

        self.mu = mu
        self.sigma = sigma
        self.mixture = mixture
        self.data = []
        self.N = N
        self.Ns = [int(x*N) for x in mixture]
        self.k = len(self.mu)

        if sum(self.Ns) != N:
            print('Warning: rounding mixture ratio. total N will be %s' %
                    sum(self.Ns))

        for m, s, n in zip(self.mu, self.sigma,self.Ns):
            data = pylab.normal(m,s,size=n)
            self.data.extend(data)

    def hist(self, bins=30, normed=True):
        pylab.hist(self.data, bins=bins, normed=normed)


class GaussianMixtureModel(object):
    def __init__(self, k=2):
        self.k = k

    def pdf(self, x, params):
        """Expected parameters are


        mu, sigma, pi, mu2, sigma2, pi2, ...
        """
        assert divmod(len(params), 3)[1] == 0
        assert len(params) >= 3 * self.k
        k = len(params) / 3

        pis = np.array(params[2::3])
        pis /= pis.sum()
        # !!! sum pi must equal 1 otherwise may diverge badly
        data = 0
        for i in range(0, k):
            mu, sigma, pi_ = params[i*3: (i+1)*3]
            pi_ = pis[i]
            data += pi_ * pylab.normpdf(x, mu, sigma)

        return data

    def log_likelihood(self, params, sample):
        return -1 * pylab.log(self.pdf(sample, params)).sum()

class Fitting(object):
    def __init__(self, data, model):
        self.data = np.array(data)
        self.model = model
        self.size = float(len(self.data))

    def plot(self, normed=True, N=1000, Xmin=None, Xmax=None, bins=50):
        pylab.hist(self.data, normed=normed, bins=bins)
        if Xmin is None:
            Xmin = self.data.min()
        if Xmax is None:
            Xmax = self.data.max()
        X = pylab.linspace(Xmin, Xmax, N)

        pylab.plot(X, [self.model.pdf(x, self.results.x) for x in X])


class MixtureFitting(Fitting):
    """

        from biokit.stats.mixture import Mixture
        m = Mixture(mu=[0,0.6], sigma=[0.08,0.12])
        m.hist()

        gmm = GaussianMixtureModel()

        mf = MixtureFitting(m.data, gmm)
        mf.minimize(guess=[])


    """
    def __init__(self, data, model, method='Nelder-Mead'):
        """

        Here we use the function minimize() from scipy.optimization. 
        The list of
        (currently) available minimization methods is 'Nelder-Mead' (simplex),
        'Powell', 'CG', 'BFGS', 'Newton-CG',> 'Anneal', 'L-BFGS-B' (like BFGS
                but bounded), 'TNC', 'COBYLA', 'SLSQPG'.

        """
        super(MixtureFitting, self).__init__(data, model)
        devtools.check_param_in_list(method, ['Nelder-Mead',
            'Powell', 'CG', 'BFGS', 'Newton-CG', 'Anneal', 'L-BFGS-B'])
        self.method = method

    def estimate(self, guess=None, method=None, maxfev=2e4, maxiter=1e3):
        """guess is a list of parameters as expected by the model"""

        if method is None:
            method = self.method

        assert guess is not None
        assert len(guess)

        res = minimize(self.model.log_likelihood, x0=guess, args=(self.data,), 
            method=method, options=dict(maxiter=maxiter, maxfev=maxfev))
        self.results = res
        return res



class EM(Fitting):

    def __init__(self, data, model, max_iter=100):
        super(EM, self).__init__(data, model)

        self.max_iter = max_iter

    def estimate(self, guess):
        #
        # Initial guess of parameters and initializations
        p0 = guess
        mu1, sig1, pi_1, mu2, sig2, pi_2 = p0

        devtools.check_range(mu1, self.data.min(), self.data.max())
        devtools.check_range(mu2, self.data.min(), self.data.max())

        mu = np.array([mu1, mu2])
        sig = np.array([sig1, sig2])
        pi_ = np.array([pi_1, 1-pi_1])

        gamma = np.zeros((2, self.size))
        N_ = np.zeros(2)
        p_new = p0

        # EM loop
        counter = 0
        converged = False
        while not converged:
        # Compute the responsibility func. and new parameters
            for k in [0, 1]:

                gamma[k, :] = pi_[k]*pylab.normpdf(self.data, mu[k], sig[k])/self.model.pdf(self.data, p_new)
                N_[k] = 1.*gamma[k].sum()
                mu[k] = sum(gamma[k]*self.data)/N_[k]
                sig[k] = pylab.sqrt( sum(gamma[k]*(self.data - mu[k])**2)/N_[k] )

                #N_[k] += 1
                pi_[k] = N_[k] /  self.size

            p_new = [mu[0], sig[0], pi_[0], mu[1], sig[1], pi_[1]]

            assert abs(N_.sum() - self.size)/self.size < 1e-6
            assert abs(pi_.sum() - 1) < 1e-6

            # Convergence check
            counter += 1
            converged = counter >= self.max_iter
        self.results = {'x': p_new}
        from easydev import AttrDict
        self.results = AttrDict(**self.results)







