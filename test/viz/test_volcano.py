

def test1():
    import numpy as np
    fc = np.random.randn(1000)
    pvalue = np.random.randn(1000)
    from biokit import Volcano
    v = Volcano(fc, -np.log10(pvalue**2))
    v.plot(pvalue_threshold=3)


