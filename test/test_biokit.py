import biokit
from nose.plugins.attrib import attr


@attr("skiptravis")
def test_biokit():
    import biokit
