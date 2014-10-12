from biokit.rtools import bool2R, RSession


__all__ = ["biocLite"]


def biocLite(package=None, suppressUpdates=True):
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
    from biokit.viz.rtools import rcode
    code = """source("http://bioconductor.org/biocLite.R")\n"""

    # without a package, biocLite performs an update of the installed packages
    if package == None:
        rcode += """biocLite(suppressUpdates=%s) """ % (
            rtools.bool2R(suppressUpdates))
    else:
        # if not found, no error is returned...
        rcode += """biocLite("%s", suppressUpdates=%s) """ % (
            package,
            rtools.bool2R(suppressUpdates))
    r = RSession()
    r.run(code)
    return True



class RPackage(object):
    def __init__(self, name, require="0.0", install=False, verbose=False):

        self.name = name
        self.package = None     # the R object linking to the R package
        self.require = require  # the required version
        self.requirement = None # is the required version found ?
        self.installed = None   # is it installed
        #self.logging = Logging("INFO")
        #if verbose == True:
        #    self.logging.level = "INFO"
        #else:
        #    self.logging.level = "WARNING"
        self._load()

    def _load(self):
        pass

    def _get_version(self):
        v = self.session.run("""version = packageVersion("%s")""" % (self.name))[0]
        v = [str(x) for x in v]
        return ".".join(v)
    version = property(_get_version)


    def __str__(self):
        pass
        #r.run("""d = installed.packages()""")





