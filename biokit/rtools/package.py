import tempfile
try:
    from urllib.request import urlopen
    from urllib.error import HTTPError, URLError
except:
    from urllib2 import urlopen, HTTPError, URLError


import os.path

from biokit.rtools import bool2R, RSession
from distutils.version import StrictVersion
from easydev import Logging, TempFile


__all__ = ["get_R_version", "biocLite", "RPackage", 
    'install_package', 'RPackageManager']


def install_package(query, dependencies=False, verbose=True,
    repos = "http://cran.univ-paris1.fr/"):
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
        if verbose:
            print("Trying from the web ?")
        data = urlopen(query)
        fh = TempFile(suffix=".tar.gz")
        with open(fh.name, 'w') as fh:
            for x in data.readlines():
                fh.write(x)
        code = """install.packages("%s", dependencies=%s """ % \
            (fh.name, bool2R(dependencies))
        code += """ , repos=NULL) """
        session.run(code)

    except Exception as err:
        if verbose:
            print(err)
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

    .. note:: R version includes dashes, which are not recognised
       by distutils so they should be replaced. 
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
            if self._get_val_version(self.version) >= self._get_val_version(self.version_required):
                pass
            else:
                print("Found %s (version %s) but version %s required." % (
                    self.name, self.version, self.version_required))

    def _get_val_version(self, version):
        return StrictVersion(version.replace("-", "a"))

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
        try:
            s = s.replace("\n", "")
            df = eval(s)
        except:
            df = s

        df.set_index('Package', inplace=True)
        self._packages = df.copy()

        # Now, fetch was is possible to install from the default cran repo
        code = """rvar_status=packageStatus(repos="%s/src/contrib")"""
        code = code % self.cran_repos

        self.session.run(code)
        s = self.session.rvar_status

        # FIXME.
        try:
            s = s.replace("\n", "")
            res = eval(s)
        except:
            res = s
        res['inst'].set_index('Package', inplace=True)
        res['avail'].set_index('Package', inplace=True)
        self._status = res

    def update(self):
        """If you install/remove packages yourself elsewhere, you may need to 
        call this function to update the package manager"""
        try:
            #self.session.reconnect()          
            self._update()
        except:
            self.logging.warning("Could not update the packages. Call update() again")

    def _compat_version(self, version):
        return version.replace("-", "a")

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

    def get_package_latest_version(self, package):
        """Get latest version available of a package"""
        return self.available['Version'].ix[package]

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
                self.logging.info("Installing %s" % pkg)
                if self.is_installed(pkg) is False:
                    biocLite(pkg, suppressUpdates, verbose=verbose)
        else: # trying other cases (e.g., None updates biocLite itself). 
            biocLite(package, suppressUpdates, verbose=verbose)
        self.update()

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
        if self._get_version(currentVersion) >= self._get_version(version):
            return True
        else:
            return False

    def _install_package(self, packageName, dependencies=True):
        """Installs one or more CRAN packages
        
        .. todo:: check if it is already available to prevent renstallation ?
        """

        repos = self.cran_repos
        # if this is a source file we want to reset the repo
        if isinstance(packageName, str):
            packageName = [packageName]
        for pkg in packageName:
            if self.is_installed(pkg) is False:
                self.logging.info("Package not found. Installing %s..." % pkg)
                install_package(pkg, dependencies=dependencies, 
                        repos=repos)
            else:
                self.logging.info("Package %s found. " % pkg)
                install_package(pkg, dependencies=dependencies, 
                        repos=repos)
        self.update()

    def install(self, pkg, require=None, update=True, reinstall=False):
        """install a package automatically scanning CRAN and biocLite repos

        if require is not set and update is True, when a newest version of a package
        is available, it is installed

        """
        from easydev import to_list
        pkgs = to_list(pkg)
        for pkg in pkgs:
            self._install(pkg, require=require, update=update, reinstall=reinstall)

    def _install(self, pkg, require=None, update=update, reinstall=False):
        # LOCAL file
        if self._isLocal(pkg):
            # if a local file, we do not want to jump to biocLite or CRAN. Let
            # us install it directly. We cannot check version yet so we will
            # overwrite what is already installed
            self.logging.warning("Installing from source")
            self._install_package(pkg)
            return

        # From CRAN
        if self.is_installed(pkg):
            currentVersion = self.get_package_version(pkg)
            # if not provided, require should be the latest version
            if require is None and update is True:
                try:
                    require = self.get_package_latest_version(pkg)
                except:
                    # a non-cran package (bioclite maybe)
                    pass

            if require is None:
                self.logging.info("%s already installed with version %s" % \
                    (pkg, currentVersion))
                return
            
            # if require is not none, is it the required version ?
            if self._get_version(currentVersion) >= self._get_version(require) and reinstall is False:
                self.logging.info("%s already installed with required version %s" \
                    % (pkg, currentVersion))
                # if so, nothing to do
            else:
                # Try updating
                self.logging.info("Updating")
                self._install_package(pkg)
                if require is None:
                    return
                currentVersion = self.get_package_version(pkg)
                if self._get_version(currentVersion) < self._get_version(require):
                    self.logging.warning("%s installed but current version (%s) does not fulfill your requirement" % \
                        (pkg, currentVersion))

        elif pkg in self.available.index:
            self._install_package(pkg)
        else:
            # maybe a biocLite package ?
            # require is ignored. The latest will be installed
            self.logging.info("Trying to find the package on bioconductor")
            self.biocLite(pkg)
            if require is None:
                return
            currentVersion = self.get_package_version(pkg)
            if self._get_version(currentVersion) >= self._get_version(require):
                self.logging.warning("%s installed but version is %s too small (even after update)" % \
                    (pkg, currentVersion, require))

    def _get_version(self, version):
        # some pacakge do not use the correct version convention
        try:
            return StrictVersion(version)
        except:
            try:
                return StrictVersion(version.replace("-", "a"))
            except:
                # snowfall package example was 1.86-6.1
                # This becomes 1.86a61  which is not great but not workaround
                # for now
                left, right = version.split("-")
                version = left + "a" + right.replace('.', '')
                return StrictVersion(version)

    def is_installed(self, pkg_name):
        if pkg_name in self.installed.index:
            return True
        else:
            return False


