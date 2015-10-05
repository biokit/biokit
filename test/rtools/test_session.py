from biokit.rtools import session
from nose.plugins.attrib import attr

@attr('Ronly')
def test_session():

    sess = session.RSession()
    print(sess)
    sess.get_version()
    try:
        sess.reconnect()
        assert False
    except:
        assert True


@attr('Ronly')
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

