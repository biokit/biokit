"""DNA sequence"""
import string

"""
import os
import ctypes
#            gcc -O2 complement.c  --shared -Wl,-soname,complement 
#                -rdynamic -o complement.so -fPIC -I/usr/include/python2.7 
from os.path import join as pj

p = os.path.abspath(os.path.dirname(__file__))
try:
    cseqkit = ctypes.CDLL("complement.so")
    cseqkit.dna_complement.restype = ctypes.c_char_p
except:
    try:
        cseqkit = ctypes.cdll.LoadLibrary(pj(p, "complement.so"))
        cseqkit.dna_complement.restype = ctypes.c_char_p
    except:
        print("coudl not install lib")
"""
from biokit.sequence.seq import Sequence


__all__ = ['DNA']


class DNA(Sequence):
    """a DNA :class:`~biokit.sequence.seq.Sequence`. 

    You can add DNA sequences together::

        >>> from biokit import DNA
        >>> s1 = DNA('ACGT')
        >>> s2 = DNA('AAAA')
        >>> s1 + s2
        Sequence: ACGTAAAA (length 8)


    """
    def __init__(self, data=''):
        super(DNA, self).__init__(data)
        self.symbols = 'ACGTacgt'
        try:
            self._translate = string.maketrans('ACGTacgt', 'TGCAtgca')
        except:
            self._translate = bytes.maketrans(b'ACGTacgt', b'TGCAtgca')
        self._type = 'DNA'

    def get_complement(self):
        compl = self._data.translate(self._translate)
        return DNA(compl)
    complement = property(get_complement)

    def get_reverse_complement(self):
        complement = self.get_complement()
        return DNA(complement._data[::-1])
    reverse_complement = property(get_reverse_complement)
    
    #def _get_complement_in_c(self):
    #    return cseqkit.dna_complement(self.sequence, len(self.sequence))
    #complement2 = property(_get_complement_in_c)
    #
    #def get_complement_c(self):
    #    print("Experimetal. Not faster than Python...")
    #    return cseqkit.dna_complement(self._data, self._N)

    def gc_content(self, letters='CGS'):
        """Returns the G+C content in percentage.

        Copes mixed case sequences, and with the ambiguous nucleotide S (G or C)
        when counting the G and C content.  

        ::

            >>> from biokit.sequence.dna import DNA
            >>> d = DNA("ACGTSAAA")
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

    def get_rna(self):
        from biokit.sequence.rna import RNA
        # here a copy is made
        seq = self._data.replace('T', 'U')
        seq = seq.replace('t', 'u')
        return RNA(seq)





