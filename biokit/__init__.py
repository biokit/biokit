__version__ = "0.1.2"
import pkg_resources
try:
    version = pkg_resources.require(biokit)[0].version
except:
    version = __version__

# Creates the data directory if it does not exist
from easydev import CustomConfig
biokitPATH = CustomConfig("biokit").user_config_dir


from biokit import viz
from biokit import io
from biokit import services

from biokit.viz import *
from biokit.services import EUtils, KEGG, UniProt

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
    sequana_path = easydev.get_package_location('biokit')
    share = os.sep.join([sequana_path , "biokit", 'data'])
    # in the code one may use / or \ 
    if where:
        filename = os.sep.join([share, where, filename])
    else:
        filename = os.sep.join([share, filename])
    if os.path.exists(filename) is False:
        raise Exception('unknown file %s' % filename)
    return filename


