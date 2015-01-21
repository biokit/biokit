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

        for m, s, n in zip(self.mu, self.sigma, self.Ns):
            data = pylab.normal(m, s, size=n)
            self.data.extend(data)

    def plot(self, bins=30, normed=True):
        self.hist(bins=bins, normed=normed)

    def hist(self, bins=30, normed=True):
        pylab.hist(self.data, bins=bins, normed=normed)


class GaussianMixtureModel(object):
    def __init__(self, k=2):
        self.k = k

    def pdf(self, x, params, normalise=True):
        """Expected parameters are


        mu, sigma, pi, mu2, sigma2, pi2, ...
        """
        assert divmod(len(params), 3)[1] == 0
        assert len(params) >= 3 * self.k
        k = len(params) / 3

        self.k = k

        pis = np.array(params[2::3])
        if normalise is True:
            pis /= pis.sum()
        # !!! sum pi must equal 1 otherwise may diverge badly
        data = 0
        for i in range(0, k):
            mu, sigma, pi_ = params[i*3: (i+1)*3]
            pi_ = pis[i]
            if sigma != 0:
                data += pi_ * pylab.normpdf(x, mu, sigma)
        return data

    def log_likelihood(self, params, sample):
        return -1 * pylab.log(self.pdf(sample, params)).sum()


class Fitting(object):
    def __init__(self, data, k=2, method='Nelder-Mead'):
        self.data = np.array(data)
        self.size = float(len(self.data))
        self._k = k
        self._model = None
        self._method = method
        # initialise the model
        self.k = k

    def _get_method(self):
        return self._method
    def _set_method(self, method):
        devtools.check_param_in_list(method, ['Nelder-Mead',
            'Powell', 'CG', 'BFGS', 'Newton-CG', 'Anneal', 'L-BFGS-B'])
        self._method = method
    method = property(_get_method, _set_method)

    def _get_k(self):
        return self._k
    def _set_k(self, k):
        assert k>0
        gmm = GaussianMixtureModel(k=k)
        self._k = k
        self._model = gmm
    k = property(_get_k, _set_k)

    def _get_model(self):
        return self._model
    model = property(_get_model)

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
            pylab.plot(X, [pi_ * pylab.normpdf(x, mu, sigma) for x in X], 'g--', alpha=0.5)


class GaussianMixtureFitting(Fitting):
    """

        from biokit.stats.mixture import Mixture
        m = Mixture(mu=[0,0.6], sigma=[0.08,0.12])
        m.hist()

        gmm = GaussianMixtureModel()

        mf = GaussianMixtureFitting(m.data, gmm)
        mf.minimize(guess=[])


    """
    def __init__(self, data, k=2, method='Nelder-Mead'):
        """

        Here we use the function minimize() from scipy.optimization. 
        The list of
        (currently) available minimization methods is 'Nelder-Mead' (simplex),
        'Powell', 'CG', 'BFGS', 'Newton-CG',> 'Anneal', 'L-BFGS-B' (like BFGS
                but bounded), 'TNC', 'COBYLA', 'SLSQPG'.

        """
        super(GaussianMixtureFitting, self).__init__(data, k=k, method=method)

    def estimate(self, guess=None, k=None, maxfev=2e4, maxiter=1e3,
            bounds=None):
        """guess is a list of parameters as expected by the model
        
        
        guess = {'mus':[1,2], 'sigmas': [0.5, 0.5], 'pis': [0.3, 0.7]  }

        """

        if k is not None:
            self.k = k

        if guess is None:
            # estimate the mu/sigma/pis from the data
            guess = self.get_guess()

        res = minimize(self.model.log_likelihood, x0=guess, args=(self.data,), 
            method=self.method, options=dict(maxiter=maxiter, maxfev=maxfev),
            bounds=bounds)
        self.results = res
        pis = np.array(self.results.x[2::3])
        if sum(pis<0) >0:
            unstable = True
            pis /= pis.sum()
            print("Unstable... found negative pis (k=%s)" % self.k)
        else:
            unstable = False
            pis /= pis.sum()

        k = len(self.results.x)/3
        params = []
        for i in range(0, k):
            params.append(self.results.x[i*3])
            params.append(self.results.x[(i*3+1)])
            params.append(pis[i])
        self.results.x = params 

        self.results.likelihood = pylab.exp(-1*self.model.log_likelihood(params, self.data))
        if self.results.likelihood and unstable is False:
            self.results.AIC = criteria.AIC(self.results.likelihood, self.k)
            self.results.AICc = criteria.AICc(self.results.likelihood, self.k, self.data.size)
            self.results.BIC = criteria.BIC(self.results.likelihood, self.k, self.data.size)
        else:
            self.results.AIC = 1000
            self.results.AICc = 1000
            self.results.BIC = 1000

        self.results.pis = self.results.x[2::3]
        self.results.sigmas = self.results.x[1::3]
        self.results.mus = self.results.x[0::3]

        #TODO normalise pis

        return res



class EM(Fitting):

    def __init__(self, data, model=None, max_iter=100):
        if model is None:
            model = GaussianMixtureModel(k=2)
        super(EM, self).__init__(data, model)
        self.max_iter = max_iter

    def estimate(self, guess=None, k=2):
        #
        self.k = k
        # Initial guess of parameters and initializations
        if guess is None:
            # estimate the mu/sigma/pis from the data
            guess = self.get_guess()

        mu = np.array(guess[0::3])
        sig = np.array(guess[1::3])
        pi_ = np.array(guess[2::3])
        N_ = len(pi_)

        gamma = np.zeros((N_, self.size))
        N_ = np.zeros(N_)
        p_new = guess

        # EM loop
        counter = 0
        converged = False

        self.mus = []
        while not converged:
        # Compute the responsibility func. and new parameters
            for k in range(0, self.k):
                # unstable if eslf.model.pdf is made of zeros


                if self.model.pdf(self.data, p_new,normalise=False).sum()!=0:
                    gamma[k, :] = pi_[k]*pylab.normpdf(self.data, mu[k],
                        sig[k])/(self.model.pdf(self.data, p_new, normalise=False))
                else:
                    gamma[k, :] = pi_[k]*pylab.normpdf(self.data, mu[k],
                        sig[k])/(self.model.pdf(self.data, p_new,
                            normalise=False)+1e-6)
                N_[k] = 1.*gamma[k].sum()
                mu[k] = sum(gamma[k]*self.data)/N_[k]
                sig[k] = pylab.sqrt( sum(gamma[k]*(self.data - mu[k])**2)/N_[k] )
                #N_[k] += 1
                pi_[k] = N_[k] /  self.size

            self.results = {'x': p_new, 'nfev':counter, 'success': converged}

            p_new = [(mu[x], sig[x], pi_[x]) for x in range(0, self.k)]
            p_new = list(pylab.flatten(p_new))

            self.status = True
            try:
                assert abs(N_.sum() - self.size)/self.size < 1e-6
                assert abs(pi_.sum() - 1) < 1e-6
            except:
                print("issue arised at iteration %s" % counter)
                self.debug = {'N':N_, 'pis':pi_}
                self.status = False
                break
                
            self.mus.append(mu)

            # Convergence check
            counter += 1
            converged = counter >= self.max_iter

        self.gamma = gamma

        if self.status is True:
            self.results = {'x': p_new, 'nfev':counter, 'success': converged}


        self.results = AttrDict(**self.results)




class AdaptativeMixtureFitting(object):
    def __init__(self, data, method='Nelder-Mead'):
        self.fitting = GaussianMixtureFitting(data, method=method)

    def run(self, kmin=1, kmax=6, criteria='AICc'):
        self.all_results = {}
        self.x = []

        for k in range(kmin, kmax+1):
            self.fitting.estimate(k=k)

            # here ritteria does not matter. if one fails, all fail
            if self.fitting.results['AIC'] != 1000:
                self.x.append(k)
                self.all_results[k] = self.fitting.results.copy()

        m = np.array([self.all_results[x][criteria] for x in self.x]).min()
        index = np.array([self.all_results[x][criteria] for x in self.x]).argmin()
        print('Found min ', m, 'for index ',index+1)
        self.best_k = self.x[index ]
        self.min_value = m


    def plot(self, criteria='AICc'):
        
        pylab.plot(self.x, [self.all_results[x]['BIC'] for x in self.x], 'o-', label='BIC')
        pylab.plot(self.x, [self.all_results[x]['AIC'] for x in self.x], 'o-',  label='AIC')
        pylab.plot(self.x, [self.all_results[x]['AICc'] for x in self.x], 'o-', label='AICc')

        m = np.array([self.all_results[x][criteria] for x in self.x]).min()
        # [exp((m-this[criteria])/2) for this in amf.all_results]

        pylab.axhline(m - pylab.log(0.9)*2, color='k', label='90% equi-probability', alpha=0.9)
        pylab.axhline(m - pylab.log(0.5)*2, color='k', label='50% equi-probability', alpha=0.5)
        pylab.axhline(m - pylab.log(0.3)*2, color='k', label='30% equi-probability', alpha=0.3)

        pylab.legend()


    def diagnostic(self, kmin=1, kmax=8, k=None, ymax=None):
        self.run(kmin=kmin, kmax=kmax); 
        pylab.clf()
        pylab.subplot(3,1,2);
        self.plot()
        mf = GaussianMixtureFitting(self.fitting.data)
        if k is None:
            mf.estimate(k=self.best_k)
        else:
            mf.estimate(k=k)
        pylab.subplot(3,1,1)
        mf.plot()
        if ymax is not None:
            pylab.ylim([0, ymax])

        pylab.subplot(3,1,3)
        min_value = np.array([self.all_results[x]['AICc'] for x in self.x]).min()
        pylab.plot(self.x, [pylab.exp((min_value-self.all_results[k]['AICc'])/2)
            for k in  self.x], 'o-', label='AICc')
        min_value = np.array([self.all_results[x]['AIC'] for x in self.x]).min()
        pylab.plot(self.x, [pylab.exp((min_value-self.all_results[k]['AIC'])/2)
            for k in  self.x], 'o-', label='AIC')
        
        pylab.xlabel('probability of information loss (based on AICc')
        pylab.legend()


        


