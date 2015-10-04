# import collections
import string

from biokit.sequence.seq import Sequence


class Peptide(Sequence):
    """a Peptide :class:`~biokit.sequence.seq.Sequence`. 

    You can add Peptide sequences together::

        >>> from biokit import DNA
        >>> s1 = Peptide('ACGT')
        >>> s2 = Peptide('AAAA')
        >>> s1 + s2
        Sequence: ACGTAAAA (length 8)

    .. note:: redundant with Sequence but may evolve in the future.
    """
    def __init__(self, data):
        super(Peptide, self).__init__(data)
        self.symbols = 'ACGTacgt'
        self._translate = string.maketrans('ACGTacgt', 'TGCAtgca')




