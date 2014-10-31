import pandas as pd
import collections
import string
import os
import ctypes

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






class DNA(pd.Series):
    """A Series to store and count DNA nucleotides


        >>> d = DNA("AGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGATTAAAAAAAGAGTGTCTGATAGCAGC")
        >>> d.count()
        A    20
        C    12
        G    17
        T    21
        dtype: int64

    You can append new nucleotides using :meth:`append`.

    .. todo:: A+B works. What about an append inplace ?




    An RNA string is a string formed from the alphabet containing 'A', 'C', 'G', and 'U'.

    Given a DNA string t corresponding to a coding strand, its transcribed RNA string u is 
    formed by replacing all occurrences of 'T' in t with 'U' in u. The :


    In DNA strings, symbols 'A' and 'T' are complements of each other, as are 'C' and 'G'.
    The reverse complement of a DNA string s is the string sc formed by reversing the symbols of s, 
    then taking the complement of each symbol (e.g., the reverse complement of "GTCA" is "TGAC").

Given: A DNA string s of length at most 1000 bp.

Return: The reverse complement sc of s.


    The GC-content of a DNA string is given by the percentage of symbols in the string that 
    are 'C' or 'G'. For example, the GC-content of "AGCTATAG" is 37.5%. Note that the reverse 
    complement of any DNA string has the same GC-content.






    """
    symbols = ["A", "C", "G", "T"]
    cbases = {"T":"A", "G":"C", "A":"T", "C":"G"}
    def __init__(self, sequence, dtype='str'):
        #self._check_sequence(sequence)
        super(DNA, self).__init__(sequence)
        #self.df = pd.DataFrame(self, columns=["letter"])

    def _get_sequence(self):
        return "".join(self)
    sequence = property(_get_sequence)

    def _check_sequence(self, sequence):
        """checks that character are valid DNA symbols"""
        for i,x in enumerate(sequence):
            if x not in DNA.symbols:
                raise ValueError("found invalid symbol %s at position %s" % (x,i))

    def count(self):
        """

        :return: Series with four integers counting the respective number of times 
            the symbols "A", "C", "G" and "T" occurs.

       .. todo:: if not found, set to 0 ?
        """
        res = self.value_counts()
        return res.sort_index()

    def gc_content(self):
        return self.value_counts(normalize=True).ix[["C", "G"]].sum()

    def hist(self):
        """

        .. plot::

        """
        res = self.count()
        res.plot(kind="bar")

    def __add__(self, other):
        return DNA(list(self.append(other)))

    
    def append(self, sequence):
        self._check_sequence(sequence)
        N = len(self)
        for i,x in enumerate(sequence):
            self[N+i] = x


    def _get_rna(self):
        rna = self.replace("T", "U")
        return rna
    rna = property(_get_rna)

    def _get_complement(self):
        """biopython

        """
        import string
        trans = string.maketrans('ACGTagct', 'TGCAtgca')
        ldna = "".join(self)
        return ldna.translate(trans)
    complement = property(_get_complement)

    def _get_complement2(self):
        """ 
        gcc -O2 complement.c  --shared -Wl,-soname,complement 
            -rdynamic -o complement.so -fPIC -I/usr/include/python2.7 
            
        """
        return cseqkit.dna_complement(self.sequence, len(self.sequence))
    complement2 = property(_get_complement2)

    def get_complement(self, sequence):
        return cseqkit.dna_complement(sequence, len(sequence))

    def _get_reverse_complement(self):
        return self.complement.sort_index(ascending=False).reset_index(drop=True)
    reverse_complement = property(_get_reverse_complement)


    def hamming_distance(self, other):
        """
        # other can be a DNA isntance or a string

Given two strings s and t of equal length, the Hamming distance between s and t, denoted dH(s,t), is the number of corresponding symbols that differ in s and t. See Figure 2.

GAGCCTACTAACGGGAT
CATCGTAATGACGGCCT

Sample Output

7

        """
        return (self!=other).sum()

def get_test_seq(expectedLength=1e6):
    factor = int(expectedLength / 50.) #100 is the length of the small string

    subseq = "AGCTTTTCATTCTGACTGCAACGGGCAATATGTCAGTGTCTCGTTGCAAA"
    sequence = "".join([subseq]*factor)
    return sequence


    

