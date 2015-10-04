import pandas as pd
import collections
import string
import os
import collections


__all__ = ['Sequence']


class Sequence(object):
    """Common data structure to all sequences (e.g., :meth:`~biokit.sequence.dna.DNA`)

    A sequence is a string contained in the :attr:`_data`. If you manipulate this attribute, 
    you should also changed the :attr:`_N` (length of the string) and set :attr:`_counter` to 
    None. 

    Sequences can be concatenated easily. You can also add a string or numpy array or pandas
    time series to an existing sequence::

        d1 = Sequence('ACGT')
        d2 = Sequence('ACGT')

    Note that there is a :meth:`check` method, which is not called during the instanciation
    but is called when adding sequences together. Each type of sequence (e.g., Sequence, DNA, RNA)
    has its own symbols. So you cannot add a DNA sequence with a RNA sequence for instance. Those are
    valid operation::

        >>> d1 = Sequence('ACGT')
        >>> d1 += 'AAAA'
        >>> d1 + d1
        >>> "AAAA" + d1




    """
    def __init__(self, data=''):
        if isinstance(data, str):
            self._data = data
        elif isinstance(data, Sequence):
            self._data = data._data
        else:
            # assume it is a list or numpy array or pandas TimeSeries
            self._data = "".join(data)

        self._N = len(self._data)
        self._counter = None
        try:
            #python2
            self.symbols = string.punctuation + string.letters
        except:
            # python3
            self.symbols = string.punctuation + string.ascii_letters



        #: check the sequence contains valid symbols if this is True
        self._check = False
    
    def __len__(self):
        return self._N

    def _get_sequence(self):
        return self._data[:]
    sequence = property(_get_sequence, 
            doc="returns a copy of the sequence")

    def _get_count(self):
        if self._counter is None:
            self._counter = collections.Counter(self._data)
        return self._counter
    counter = property(_get_count, doc="return counter of the letters")

    def histogram(self):
        import pylab
        pylab.clf(); 
        import pandas as pd
        pd.TimeSeries(self.counter).plot(kind='bar')

    def hamming_distance(self, other):
        """Return hamming distance between this sequence and another sequence
        
        The Hamming distance between s and t, denoted dH(s,t), is the number of 
        corresponding symbols that differ in s and t.

        ::

            >>> d1 = 'GAGCCTACTAACGGGAT'
            >>> d2 = 'CATCGTAATGACGGCCT'
            >>> s = Sequence(d1)
            >>> s.hamming_distance(d2)
            7
        """
        # TODO:: convert to appropriate sequence.
        return sum(1 for x,y in zip(self._data, other._data) if x!=y)

    def upper(self):
        """convertes sequence string to uppercase (inplace)"""
        self._data = self._data.upper()
    
    def lower(self):
        """convertes sequence string to lowercase (inplace)"""
        self._data = self._data.lower()
    
    def _check_sequence(self):
        """checks that characters are valid symbols"""
        for i, x in enumerate(self._data):
            if x not in self.symbols:
                raise ValueError("found invalid symbol %s at position %s" % (x,i))

    def __repr__(self):
        if self._N > 10:
            return "Sequence: %s ... (length %s) " % (self.sequence[0:10], self._N)
        else:
            return "Sequence: %s (length %s) " % (self.sequence, self._N)

    def __str__(self):
        if self._N > 10:
            return "Sequence: %s ... (length %s) " % (self.sequence[0:10], self._N)
        else:
            return "Sequence: %s (length %s) " % (self.sequence, self._N)

    def __convert_to_compat(self, other):
        from biokit.sequence.rna import RNA
        from biokit.sequence.dna import DNA

        if isinstance(self, RNA):
            other = RNA(other)
        elif isinstance(self, DNA):
            other = DNA(other)
        elif isinstance(self, Sequence):
            other = Sequence(other)
        if self._check is True:
            other._check_sequence()
        return other

    def __add__(self, other):
        # input may be a string or list, in which case we need to convert to a sequence
        if isinstance(other, Sequence) is False:
            other = self.__convert_to_compat(other)
        elif type(other) != type(self):
            raise TypeError('incompatible sequences %s versus %s' % (type(other), type(self)))

        # now let us add the 2 sequences
        return self.__convert_to_compat(self._data + other._data)

    def __radd__(self, other):
        """operator other + self"""
        if isinstance(other, Sequence) is False:
            other = self.__convert_to_compat(other)
        elif type(other) != type(self):
            raise TypeError('incompatible sequences %s versus %s' % (type(other), type(self)))

        # now let us add the 2 sequences
        return self.__convert_to_compat(other._data + self._data)

    def __iadd__(self, other):
        if isinstance(other, Sequence) is False:
            other = self.__convert_to_compat(other)
        elif type(other) != type(self):
            raise TypeError('incompatible sequences %s versus %s' % (type(other), type(self)))

        # now let us add the 2 sequences
        self._data += other._data
        self._N = self._N + other._N
        return self

        


