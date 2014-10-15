import tempfile
import urllib2
import os.path

from biokit.rtools import bool2R, RSession
from distutils.version import StrictVersion


__all__ = ["get_R_version", "biocLite", "RPackage", 'install_package']


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


    .. todo:: packagemanager with bioclite included.

    """

    session = RSession(dump_stdout=verbose)

    # Is it a local file?
    if os.path.exists(query):
        filename = query[:]
    else:
        try:
            print("TRY")
           # is it a valid URL ? If so, it should be a kind of source package
            data = urllib2.urlopen(query)
            if verbose == True:
                print("Installing %s from %s" % (query, filename))
            code = """install.packages("%s", dependencies=%s """ % \
                (filename, bool2R(dependencies))
            if repos != None:
                code += """ , repos="%s") """ % repos
            else:
                code += """ , repos=NULL) """
            session.run(code)

        except:
            print("EXCEPT")
            print("RTOOLS warning: URL provided does not seem to exist %s. Trying from CRAN" % query)
            code = """install.packages("%s", dependencies=%s """ % \
                (query, bool2R(dependencies))

            if repos:
                code += """ , repos="%s") """ % repos
            else:
                code += ")"
            session.run(code)
            return
        # If valid URL, let us download the data in a temp file
        # get new temp filename
        handle = tempfile.NamedTemporaryFile()

        # and save the downloaded data into it before installation
        ff = open(handle.name, "w")
        ff.write(data.read())
        ff.close()
        filename = ff.name[:]



def get_R_version():
    r = RSession()
    r.run("version")
    return r.version


def biocLite(package=None, suppressUpdates=True, dump_stdout=True):
    """Install a bioconductor package

    This function does not work like the R function. Only a few options are
    implemented so far. However, you can use rcode function directly if needed.

    :param str package: name of the bioconductor package to install. If None, no
        package is installed but installed packages are updated.
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
    if package == None:
        code += """biocLite(suppressUpdates=%s) """ % (
            bool2R(suppressUpdates))
    else:
        # if not found, no error is returned...
        code += """biocLite("%s", suppressUpdates=%s) """ % (
            package,
            bool2R(suppressUpdates))
    r = RSession(dump_stdout=dump_stdout)
    r.run(code)
    return True






class RPackage(object):
    """

    ::

        >>> from biokit.rtools import package
        >>> p = package.RPackage('CellNOptR')
        >>> p.isinstalled
        True
        >>> p.version
        '1.11.3'

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

    """
    cran_repos = "http://cran.univ-lyon1.fr/"

    def __init__(self):

        self.session = RSession()


    def _installed_packages(self):
        # we do not buffer because one may install packages in between
        code = """rvar_packages = as.data.frame(installed.packages())"""
        self.session.run(code)
        s = self.session.rvar_packages
        # FIXME. these 4 lines are needed as a hack related to pyper.
        s = s.replace("\n", "")
        import numpy
        import pandas
        df = eval(s)

        df.set_index('Package', inplace=True)
        self._packages = df.copy()
        return self._packages
        #m.reshape(16,1088/16)

    def _package_status(self):
        # we do not buffer because one may install packages in between
        code = """rvar_status=packageStatus(repos="%s/src/contrib")"""
        code = code % self.cran_repos

        self.session.run(code)
        s = self.session.rvar_status

        # FIXME.
        s = s.replace("\n", "")
        import pandas
        import numpy
        res = eval(s)
        res['inst'].set_index('Package', inplace=True)
        res['avail'].set_index('Package', inplace=True)
        self._status = res

    def _get_installed(self):
        # we do not buffer because packages may be removed manually or from R of
        # using remove_packages method, ....
        self._package_status()
        return self._status['inst']
    installed = property(_get_installed, "returns list of packages installed as a dataframe")

    def _get_available(self):
        # we do not buffer because packages may be removed manually or from R of
        # using remove_packages method, ....
        self._package_status()
        return self._status['avail']
    available = property(_get_available, "returns list of packages available as a dataframe")

    def  _get_packages(self):
        # do not buffer since it may change in many places
        self._installed_packages()
        return self._packages
    packages = property(_get_packages)

    def install_packages(self, packageName, dependencies=True, repos=None):
        raise NotImplementedError

    def get_package_version(self):
        return self.packages['Version']['CellNOptR']

    def biocLite(self):
        raise NotImplementedError

    def remove(self):
        raise NotImplementedError

    def install(self):
        raise NotImplementedError


"""
    def install_packages(self, packageName, dependencies=True, repos=None,
        type=None):
        "Installs one or more CRAN packages"

        if repos == None:
            repos = self.cran_repos
        # if this is a source file we want to reset the repo
        if type == "source":
            repos = None
        if isinstance(packageName, str):
            if packageName not in self.installed['Package']:
                install_packages(packageName, dependencies=dependencies,
                    repos=repos)
        elif isinstance(packageName, list):
            for pkg in packageName:
                if pkg not in self.installed['Package']:
                    install_packages(pkg, dependencies=dependencies,
                        repos=repos)

    def biocLite(self, packageName=None,suppressUpdates=True):
        Installs one or more biocLite packages


        :param packageName: a package name (string) that will be installed from
            BioConductor. Several package names can be provided as a list. If
            packageName is set to None, all packages already installed will be
            updated.

        "
        if isinstance(packageName, str):
            if packageName not in self.installed['Package']:
                biocLite(packageName, suppressUpdates)
        elif isinstance(packageName, list):
            for pkg in packageName:
                if pkg not in self.installed['Package']:
                    biocLite(pkg, suppressUpdates)
        elif packageName == None:
            if packageName not in self.installed['Package']:
                 biocLite(None, suppressUpdates)

    def _isLocal(self, pkg):
        if os.path.exists(pkg):
            return True
        else:
            return False

    def remove_packages(self, packageName):
        code ="remove.packages("%s")"
        if isinstance(packageName, str):
            if packageName in self.installed['Package']:
                rcode(code % packageName)
            else:
                self.logging.warning("Package not found. Nothing to remove")
        elif isinstance(packageName, list):
            for pkg in packageName:
                if packageName in self.installed['Package']:
                    rcode(code % pkg)
                else:
                    self.logging.warning("Package not found. Nothing to remove")

    def require(self, pkg, version):
        "Check if a package with given version is available"

        if pkg not in self.packages:
            self.logging.info("Package %s not installed" % pkg)
            return False
        currentVersion = self.packageVersion(pkg)
        if StrictVersion(currentVersion) >= StrictVersion(version):
            return True
        else:
            return False

    def install(self, pkg, require=None):
        "install a package automatically scanning CRAN and biocLite repos


        "
        if self._isLocal(pkg):
            # if a local file, we do not want to jump to biocLite or CRAN. Let
            # us install it directly. We cannot check version yet so we will
            # overwrite what is already installed
            self.logging.warning("Installing from source")
            self.install_packages(pkg, repos=None, type="source")
            return

        if pkg in self.installed['Package']:
            currentVersion = self.packageVersion(pkg)
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
                self.install_packages(pkg, repos=self.cran_repos)
                if require == None:
                    return
                currentVersion = self.packageVersion(pkg)
                if StrictVersion(currentVersion) >= StrictVersion(require):
                    self.logging.warning("%s installed but current version (%s) does not fulfill your requirement" % \
                        (pkg, currentVersion))

        elif pkg in self.available['Package']:
            self.install_packages(pkg, repos=self.cran_repos)
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







"""
















