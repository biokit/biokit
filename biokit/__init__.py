__version__ = "0.1.2"
import pkg_resources
try:
    version = pkg_resources.require("biokit")[0].version
except:
    version = __version__

# Creates the data directory if it does not exist
from easydev import CustomConfig
biokitPATH = CustomConfig("biokit").user_config_dir

import colorlog as logger
def biokit_debug_level(level="WARNING"):
    """A deubg level setter at top level of the library"""
    assert level in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    logging_level = getattr(logger.logging.logging, level)
    logger.getLogger().setLevel(logging_level)


from biokit import viz
from biokit.viz import *



from biokit import stats
from biokit.network import *

from biokit import sequence
from biokit.sequence import *

from biokit import goid
from biokit.goid import *

from biokit import taxonomy
from biokit.taxonomy import Taxonomy


def biokit_data(filename, where=None):
    """Simple utilities to retrieve data sets from biokit/data directory"""
    import os
    import easydev
    biokit_path = easydev.get_package_location('biokit')
    share = os.sep.join([biokit_path , "biokit", 'data'])
    # in the code one may use / or \ 
    if where:
        filename = os.sep.join([share, where, filename])
    else:
        filename = os.sep.join([share, filename])
    if os.path.exists(filename) is False:
        raise Exception('unknown file %s' % filename)
    return filename


