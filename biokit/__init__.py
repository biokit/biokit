"""Main entry point to biokit


::

    import biokit as bk
    from bk import bioservices
    from bk import sequence

    from bioservices.apps import get_fasta
    fasta = get_fasta("P43403")

    seq = sequence.FASTA(fasta)
    seq.plot()

"""
__version__ = "0.1"
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




