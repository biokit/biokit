from biokit.rtools import package
from nose.plugins.attrib import attr
import create_dummy_package as dun

# This will not work on travis since you will need R


@attr('Ronly')
def test_install_packages():
    d = dun.CreateDummy()
    d()
    package.install_package('dummy/dummytest_1.0.0.tar.gz', verbose=True) 
    d._clean()


@attr('Ronly')
def test_install_packages():
    package.install_package("truncnorm")


@attr('Ronly')
def test_get_r_version():
    package.get_R_version()


@attr('Ronly')
def test_bioclite():
    package.biocLite('truncnorm')


@attr('Ronly')
def test_rpackage():
    # need to play with a pacakge. Again a dummy one would be handy
    p = package.RPackage('CellNOptR')
    p = package.RPackage('CellNOptR', version_required="2000.0")
    p = package.RPackage('CellNOptR', version_required="2000")

    p = package.RPackage('dummy')
    assert p.isinstalled is False
    print(p)


@attr('Ronly')
def test_pm():

    pm = package.RPackageManager()
    pm.packages
    pm.installed
    pm.available
