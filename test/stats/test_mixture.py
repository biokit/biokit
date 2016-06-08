from biokit.stats.mixture import GaussianMixtureModel
from biokit.stats.mixture import GaussianMixture
from biokit.stats.mixture import GaussianMixtureFitting




def test_gmm():
    gmm = GaussianMixtureModel(k=2)
    gmm.pdf(5, params=[-1,0.5,0.2,1,0.5,0.8])

def test_gmf():
    m = GaussianMixture(mu=[-2,1], sigma=[0.5,0.5], mixture=[.2,.8], N=50)
    mf = GaussianMixtureFitting(m.data)
    mf.estimate()
    mf.k = 3
    mf.estimate()
    assert mf.k == 3
    #mf.model = 'CG'
    #mf.estimate()

def test_em():
    from biokit.stats.mixture import EM
    m = GaussianMixture(mu=[-2,1], sigma=[0.5,0.5], mixture=[.2,.8], N=50)
    em = EM(m.data)
    em.estimate()
    em.plot()

def test_amf():
    from biokit.stats.mixture import AdaptativeMixtureFitting
    m = GaussianMixture(mu=[-2,1], sigma=[0.5,0.5], mixture=[.2,.8], N=50)
    amf = AdaptativeMixtureFitting(m.data)
    amf.run(kmin=1,kmax=4)


    amf.diagnostic()
