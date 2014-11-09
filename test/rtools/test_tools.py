from biokit.rtools import tools



def test_codecs():

    assert 'T' == tools.bool2R(True)
    assert 'F' == tools.bool2R(False)
    try:
        tools.bool2R('ggg')
        assert False
    except:
        assert True


def test_rcode():
    r = tools.rcode('a=1')
    assert r.a == 1 

