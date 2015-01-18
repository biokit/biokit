# source
# http://nbviewer.ipython.org/github/tritemio/notebooks/blob/master/Mixture_Model_Fitting.ipynb

from easydev import DevTools
devtools = DevTools()
from scipy.optimize import minimize, show_options
import numpy as np
import pylab
import seaborn as sns
from easydev import AttrDict

import criteria

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

        self.k = k

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
    
    def get_guess(self):
        params = {}
        m = self.data.min()
        M = self.data.max()
        range_ = M - m

        mus = [m + range_ / (self.k+1.) * i for i in range(1, self.k+1)]
        params['mus'] = mus

        sigma = range_ / float(self.k+1) / 2.
        params['sigmas'] = [sigma] * self.k

        params['pis'] = [1./self.k] * self.k

        params = [ [mu,sigma,pi]  for mu,sigma,pi in 
                    zip(params['mus'], params['sigmas'], params['pis'])]
        params = list(pylab.flatten(params))
        return params

    def plot(self, normed=True, N=1000, Xmin=None, Xmax=None, bins=50, color='red', lw=2, 
            hist_kw={'color':'#5F9EA0'}):

        pylab.hist(self.data, normed=normed, bins=bins, **hist_kw)
        if Xmin is None:
            Xmin = self.data.min()
        if Xmax is None:
            Xmax = self.data.max()
        X = pylab.linspace(Xmin, Xmax, N)

        pylab.plot(X, [self.model.pdf(x, self.results.x) for x in X], color=color, lw=lw)
            
        K = len(self.results.x)
        # The PIs must be normalised
        for i in range(0, K/3):
            mu, sigma, pi_ = self.results.x[i*3], self.results.x[i*3+1], self.results.x[i*3+2]
            #print(mu,sigma, pi_)
            pylab.plot(X, [pi_ * pylab.normpdf(x, mu, sigma) for x in X], 'g--', alpha=0.5)


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
        self.k = model.k

    def estimate(self, guess=None, method=None, maxfev=2e4, maxiter=1e3):
        """guess is a list of parameters as expected by the model
        
        
        guess = {'mus':[1,2], 'sigmas': [0.5, 0.5], 'pis': [0.3, 0.7]  }

        """

        if method is None:
            method = self.method

        if guess is None:
            # estimate the mu/sigma/pis from the data
            guess = self.get_guess()


        res = minimize(self.model.log_likelihood, x0=guess, args=(self.data,), 
            method=method, options=dict(maxiter=maxiter, maxfev=maxfev))
        self.results = res
        pis = np.array(self.results.x[2::3])
        pis /= pis.sum()
        k = len(self.results.x)/3
        params = []
        for i in range(0, k):
            params.append(self.results.x[i*3])
            params.append(self.results.x[(i*3+1)])
            params.append(pis[i])
        self.results.x = params 

        self.results.likelihood = pylab.exp(-1*self.model.log_likelihood(params, self.data))
        if self.results.likelihood:
            self.results.AIC = criteria.AIC(self.results.likelihood, self.k)
            self.results.AICc = criteria.AICc(self.results.likelihood, self.k, self.data.size)
            self.results.BIC = criteria.BIC(self.results.likelihood, self.k, self.data.size)
        else:
            self.results.AIC = 1000
            self.results.AICc = 1000
            self.results.BIC = 1000



        #TODO normalise pis

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
        self.results = {'x': p_new, 'nfev':counter, 'success': converged}
        self.results = AttrDict(**self.results)




class AdaptativeMixtureFitting(MixtureFitting):
    def __init__(self, data, method='Nelder-Mead'):
        gmm = GaussianMixtureModel(k=1) #dummy to initialise
        super(AdaptativeMixtureFitting, self).__init__(data, gmm)
        devtools.check_param_in_list(method, ['Nelder-Mead',
            'Powell', 'CG', 'BFGS', 'Newton-CG', 'Anneal', 'L-BFGS-B'])

    def run(self, kmin=1, kmax=6):
        self.all_results = []
        self.x = range(kmin, kmax+1)

        for k in range(kmin, kmax+1):
            gmm = GaussianMixtureModel(k=k)
            self.k = k
            self.model = gmm
            self.estimate()
            self.all_results.append(self.results.copy())

    def plot(self, criteria='AICc'):
        pylab.plot(self.x, [x['BIC'] for x in self.all_results], label='BIC')
        pylab.plot(self.x, [x['AIC'] for x in self.all_results], label='AIC')
        pylab.plot(self.x, [x['AICc'] for x in self.all_results], label='AICc')

        m = np.array([this[criteria] for this in self.all_results]).min()
        # [exp((m-this[criteria])/2) for this in amf.all_results]

        pylab.axhline(m - pylab.log(0.9)*2, color='k', label='90% equi-probability', alpha=0.9)
        pylab.axhline(m - pylab.log(0.5)*2, color='k', label='50% equi-probability', alpha=0.5)
        pylab.axhline(m - pylab.log(0.3)*2, color='k', label='30% equi-probability', alpha=0.3)

        pylab.legend()




