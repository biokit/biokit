from biokit.rtools import session


import pytest
import os
skiptravis = pytest.mark.skipif( "TRAVIS_PYTHON_VERSION" in os.environ,
    reason="On travis")




@skiptravis
def test_session():

    sess = session.RSession()
    print(sess)
    sess.get_version()
    try:
        sess.reconnect()
        assert False
    except:
        assert True


@skiptravis
def test_attribute():
    s = session.RSession()
    s.run("b=1")
    assert 1 == s.b
    try:
        s.c
        assert False
    except:
        assert True
    assert 1 == s.b

