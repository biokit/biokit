from biokit.rtools import package


def test_install_packages():
    # create a dummy package as a tar.gz
    # install it 
    # remove it
    pass


def test_get_r_version():
    package.get_R_version()


def test_biocLite():

    # how to test without intefering with user directory ?
    #
    pass


def test_rpackage():
    # need to play with a pacakge. Again a dummy one would be handy
    p = package.RPackage('CellNOptR')
    p = package.RPackage('CellNOptR', require="2000.0")
    p = package.RPackage('CellNOptR', require="2000")

    p = package.RPackage('dummy')
    assert p.isinstalled == False
    print(p)


def test_pm():

    pm = package.RPackageManager()
    pm.packages
    pm.installed
    pm.available
