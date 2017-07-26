from biokit.rtools import tools
import pytest
import os
skiptravis = pytest.mark.skipif( "TRAVIS_PYTHON_VERSION" in os.environ,
    reason="On travis")





@skiptravis
def test_codecs():

    assert 'T' == tools.bool2R(True)
    assert 'F' == tools.bool2R(False)
    try:
        tools.bool2R('ggg')
        assert False
    except:
        assert True

@skiptravis
def test_rcode():
    r = tools.rcode('a=1')
    assert r.a == 1 

