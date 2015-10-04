"""RNA sequence"""
import string
from biokit.sequence.seq import Sequence


__all__ = ['RNA']



class RNA(Sequence):
    def __init__(self, sequence=''):
        super(RNA, self).__init__(sequence)
        self.symbols = 'ACGUacgu'
        try:
            self._translate = string.maketrans('ACGUacgu', 'UGCAugca')
        except:
            self._translate = bytes.maketrans(b'ACGUacgu', b'UGCAugca')
        self._type = 'RNA'

    def get_complement(self):
        compl = self._data.translate(self._translate)
        return RNA(compl)
    complement = property(get_complement)

    def get_reverse_complement(self):
        complement = self.get_complement()
        return RNA(complement._data[::-1])
    reverse_complement = property(get_reverse_complement)

    def get_dna(self):
        # here a copy is made
        from biokit.sequence.dna import DNA
        seq = self._data.replace('U', 'T')
        seq = seq.replace('u', 't')
        return DNA(seq)

    def gc_content(self, letters='CGS'):
        """Returns the G+C content in percentage.

        Copes mixed case sequences, and with the ambiguous nucleotide S (G or C)
        when counting the G and C content.

        ::

            >>> from biokit.sequence.dna import RNA
            >>> d = RNA("ACGTSAAA")
            >>> d.gc_content()
            0.375


        """
        if len(self) == 0:
            denom = 1.
        else:
            denom = float(self._N)
        letters = [x.upper() for x in letters] + [x.lower() for x in letters]
        letters = list(set(letters))
        counter = sum(self._data.count(x) for x in letters)
        return 100. * counter / denom

