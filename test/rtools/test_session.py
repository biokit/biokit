from biokit.rtools import session
from nose.plugins.attrib import attr

@attr('Ronly')
def test_session():

    sess = session.RSession()
    sess.get_version()
    try:
        sess.reconnect()
        assert False
    except:
        assert True



    #sess = session.RSession(RCMD='R --quiet')
