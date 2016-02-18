from biokit.rtools import package
from nose.plugins.attrib import attr
try:
    import create_dummy_package as dun
except:
    from . import create_dummy_package as dun


# This will not work on travis since you will need R


@attr('Ronly')
def test_install_packages():
    d = dun.CreateDummy()
    d()
    package.install_package('./dummy/dummytest_1.0.0.tar.gz', verbose=True) 
    d._clean()


@attr('Ronly')
def test_install_packages():
    package.install_package("truncnorm")


@attr('Ronly')
def test_get_r_version():
    package.get_R_version()


@attr('Ronly')
def test_bioclite():
    package.biocLite()
    package.biocLite('truncnorm')


@attr('Ronly')
def test_rpackage():
    # need to play with a pacakge. Again a dummy one would be handy
    p = package.RPackage('CellNOptR')
    p = package.RPackage('CellNOptR', version_required="2000.0")
    p = package.RPackage('CellNOptR', version_required="2000")
    print(p)

    p = package.RPackage('dummy')
    assert p.isinstalled is False
    print(p)


@attr('Ronly')
def test_pm():

    pm = package.RPackageManager()
    pm.packages
    pm.installed
    pm.available
    pm.get_package_version('base')


    try:
        pm.get_package_version('whatever_is_not_installed')
        assert False
    except:
        assert True


    pm.remove('truncnorm')
    pm.biocLite('truncnorm')
    pm.biocLite(['truncnorm'])
    pm.biocLite(None)


    d = dun.CreateDummy()
    d()
    pm.install('dummy/dummytest_1.0.0.tar.gz') 
    pm.remove('dummytest')
    d._clean()

    pm.remove('truncnorm')
    pm.install('truncnorm')
    pm.install('truncnorm') # trying again with required version

