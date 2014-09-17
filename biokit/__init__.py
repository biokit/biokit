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
__version__ = '0.0.1'

from . import viz
from . import services
#from . import sequence
#from . import data
#from . import io

from .services import EUtils, KEGG, UniProt
