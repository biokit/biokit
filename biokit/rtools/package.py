import tempfile
import urllib
import os.path
from easydev import TempFile

from biokit.rtools import bool2R, RSession
from distutils.version import StrictVersion
from easydev import Logging

__all__ = ["get_R_version", "biocLite", "RPackage", 
    'install_package', 'RPackageManager']


def install_package(query, dependencies=False, verbose=True,
    repos="http://cran.univ-lyon1.fr/"):
    """Install a R package

    :param str query: It can be a valid URL to a R package (tar ball), a CRAN
        package, a path to a R package (tar ball), or simply the directory
        containing a R package source.
    :param bool dependencies:
    :param repos: if provided, install_packages automatically select the
        provided repositories otherwise a popup window will ask you to select a repo

    ::

        >>> rtools.install_package("path_to_a_valid_Rpackage.tar.gz")
        >>> rtools.install_package("http://URL_to_a_valid_Rpackage.tar.gz")
        >>> rtools.install_package("hash") # a CRAN package
        >>> rtools.install_package("path to a valid R package directory")

    .. seealso:: :class:`biokit.rtools.RPackageManager`
    """
    session = RSession(verbose=verbose)

    # Is it a local file?
    if os.path.exists(query):
        repos = 'NULL'
    else:
        repos = '"{0}"'.format(repos) # we want the " to be part of the string later on
    
    try:
        # PART for fetching a file on the web, download and install locally
        print("Trying from the web ?")
        data = urllib.request(query)
        fh = TempFile(suffix=".tar.gz")
        with open(fh.name, 'w') as fh:
            for x in data.readlines():
                fh.write(x)
        code = """install.packages("%s", dependencies=%s """ % \
            (fh.name, bool2R(dependencies))
        code += """ , repos=NULL) """
        session.run(code)

    except Exception as err:
        print(err.message)
        print("trying local or from repos")
        print("RTOOLS warning: URL provided does not seem to exist %s. Trying from CRAN" % query)
        code = """install.packages("%s", dependencies=%s """ % \
            (query, bool2R(dependencies))

        code += """ , repos=%s) """ % repos
        session.run(code)
        return

def get_R_version():
    """Return R version"""
    r = RSession()
    r.run("version")
    return r.version


def biocLite(package=None, suppressUpdates=True, verbose=True):
    """Install a bioconductor package

    This function does not work like the R function. Only a few options are
    implemented so far. However, you can use rcode function directly if needed.

    :param str package: name of the bioconductor package to install. If None, no
        package is installed but installed packages are updated. If not provided, 
        biocLite itself may be updated if needed.
    :param bool suppressUpdates: updates the dependencies if needed (default is
        False)

    :return: True if update is required or the required package is installed and
        could be imported. False otherwise.

    ::

        >>> from biokit.viz.rtools import biocLite
        >>> biocLite("CellNOptR")

    """
    code = """source("http://bioconductor.org/biocLite.R")\n"""

    # without a package, biocLite performs an update of the installed packages
    if package is None:
        code += """biocLite(suppressUpdates=%s) """ % (
            bool2R(suppressUpdates))
    else:
        # if not found, no error is returned...
        code += """biocLite("%s", suppressUpdates=%s) """ % (
            package,
            bool2R(suppressUpdates))
    r = RSession(verbose=verbose)
    r.run(code)
    

class RPackage(object):
    """

    ::

        >>> from biokit.rtools import package
        >>> p = package.RPackage('CellNOptR')
        >>> p.isinstalled
        True
        >>> p.version
        '1.11.3'

    .. todo:: do we need the version_required attribute/parameter anywhere ?
    """
    def __init__(self, name, version_required=None, install=False, verbose=False):
        self.name = name
        self.version_required = version_required  # the required version
        if self.version_required and isinstance(self.version_required, str) is False:
            raise TypeError("version_required argument must be a string e.g., 2.0, 2.0.1")
        if version_required and "." not in self.version_required:
            # trying to infer correct version
            self.version_required += '.0'

        self.session = RSession()

        code = """rvar_version = as.character(packageVersion("%s"))"""
        self.session.run(code  % (self.name))
        try:
            self._version = self.session.rvar_version
        except:
            self._version = None

        if self.version is None and install is True:
            self.install(name)
        if self.version and self.version_required:
            if StrictVersion(self.version) >= StrictVersion(self.version_required):
                pass
            else:
                print("Found %s (version %s) but version %s required." % (
                    self.name, self.version, self.version_required))

    def install(self):
        install_package(self.name)

    def _get_isinstalled(self):
        if self.version:
            return True
        else:
            return False
    isinstalled = property(_get_isinstalled)

    def _get_version(self):
        return self._version
    version = property(_get_version)

    def __str__(self):
        if self.version:
            txt = self.name + ": " + self.version
        else:
            txt = self.name
        return txt


class RPackageManager(object):
    """Implements a R package manager from Python

    So far you can install a package (from source, or CRAN, or biocLite)

    ::

        pm = PackageManager()
        [(x, pm.installed[x][2]) for x in pm.installed.keys()]


    You can access to all information within a dataframe called **packages** where
    indices are the name packages. Some aliases are provided as attributes (e.g., available, 
    installed)


    """
    cran_repos = "http://cran.univ-lyon1.fr/"

    def __init__(self, verbose=True):
        self.session = RSession()
        self.logging = Logging(verbose)
        self.logging.info('Fetching package information')
        self.update()

    def _update(self):
        # local import ?
        import numpy
        import pandas
        # figure out the installed packages first
        code = """rvar_packages = as.data.frame(installed.packages())"""
        self.session.run(code)
        s = self.session.rvar_packages
        # FIXME. these 4 lines are needed as a hack related to pyper.
        s = s.replace("\n", "")
        df = eval(s)

        df.set_index('Package', inplace=True)
        self._packages = df.copy()

        # Now, fetch was is possible to install from the default cran repo
        code = """rvar_status=packageStatus(repos="%s/src/contrib")"""
        code = code % self.cran_repos

        self.session.run(code)
        s = self.session.rvar_status

        # FIXME.
        s = s.replace("\n", "")
        res = eval(s)
        res['inst'].set_index('Package', inplace=True)
        res['avail'].set_index('Package', inplace=True)
        self._status = res

    def update(self):
        """If you install/remove packages yourself elsewhere, you may need to 
        call this function to update the package manager"""
        self._update()

    def _get_installed(self):
        # we do not buffer because packages may be removed manually or from R of
        # using remove_packages method, ....
        #self._package_status()
        return self._status['inst']
    installed = property(_get_installed, "returns list of packages installed as a dataframe")

    def _get_available(self):
        # we do not buffer because packages may be removed manually or from R of
        # using remove_packages method, ....
        #self._package_status()
        return self._status['avail']
    available = property(_get_available, "returns list of packages available as a dataframe")

    def  _get_packages(self):
        # do not buffer since it may change in many places
        return self._packages
    packages = property(_get_packages)

    def get_package_version(self, package):
        """Get version of an install package"""
        if package not in self.installed.index:
            self.logging.error("package {0} not installed".format(package))
        return self.installed['Version'].ix[package]

    def biocLite(self, package=None, suppressUpdates=True, verbose=False):
        """Installs one or more biocLite packages

        :param package: a package name (string) or list of package names (list of 
            strings) that will be installed from BioConductor. If package is set 
            to None, all packages already installed will be updated.

        """
        if isinstance(package, str):
            if package not in self.installed.index:
                biocLite(package, suppressUpdates, verbose=verbose)
        elif isinstance(package, list):
            for pkg in package:
                if pkg not in self.installed.index:
                    biocLite(pkg, suppressUpdates, verbose=verbose)
        else: # trying other cases (e.g., None updates biocLite itself). 
             biocLite(package, suppressUpdates)

    def _isLocal(self, pkg):
        if os.path.exists(pkg):
            return True
        else:
            return False

    def remove(self, package):
        """Remove a package (or list) from local repository"""
        rcode ="""remove.packages("%s")"""
        if isinstance(package, str):
            package = [package]
        for pkg in package:
            if pkg in self.installed.index:
                self.session(rcode % pkg)
            else:
                self.logging.warning("Package not found. Nothing to remove")
        self.update()

    def require(self, pkg, version):
        "Check if a package with given version is available"

        if pkg not in self.installed.index:
            self.logging.info("Package %s not installed" % pkg)
            return False
        currentVersion = self.packageVersion(pkg)
        if StrictVersion(currentVersion) >= StrictVersion(version):
            return True
        else:
            return False

    def _install_packages(self, packageName, dependencies=True):
        """Installs one or more CRAN packages
        
        
        .. todo:: check if it is already available to prevent renstallation ?
        """

        repos = self.cran_repos
        # if this is a source file we want to reset the repo
        if isinstance(packageName, str):
            packageName = [packageName]
        for pkg in packageName:
            if pkg not in self.installed.index:
                install_package(pkg, dependencies=dependencies, 
                        repos=repos)
        self.update()

    def install(self, pkg, require=None):
        """install a package automatically scanning CRAN and biocLite repos


        """
        if self._isLocal(pkg):
            # if a local file, we do not want to jump to biocLite or CRAN. Let
            # us install it directly. We cannot check version yet so we will
            # overwrite what is already installed
            self.logging.warning("Installing from source")
            self._install_packages(pkg)
            return

        if pkg in self.installed.index:
            currentVersion = self.get_package_version(pkg)
            if require == None:
                self.logging.info("%s already installed with version %s" % \
                    (pkg, currentVersion))
                return
            # nothing to do except the required version
            if StrictVersion(currentVersion) >= StrictVersion(require):
                self.logging.info("%s already installed with required version %s" \
                    % (pkg, currentVersion))
            else:
                # Try updating
                self._install_packages(pkg)
                if require == None:
                    return
                currentVersion = self.get_package_version(pkg)
                if StrictVersion(currentVersion) >= StrictVersion(require):
                    self.logging.warning("%s installed but current version (%s) does not fulfill your requirement" % \
                        (pkg, currentVersion))

        elif pkg in self.available.index:
            self._install_packages(pkg)
        else:
            # maybe a biocLite package:
            # require is ignored. The latest will be installed
            self.biocLite(pkg)
            if require == None:
                return
            currentVersion = self.packageVersion(pkg)
            if StrictVersion(currentVersion) >= StrictVersion(require):
                self.logging.warning("%s installed but version is %s too small (even after update)" % \
                    (pkg, currentVersion, require))




