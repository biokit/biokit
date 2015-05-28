"""Some utilities used in notebooks"""



class SequenceBenchmark(object):
    """Create a random sequence of ACGT
    
    ::

        s = SequenceBenchmark()
        sequence = s.create_sequence()
    
    """
    def __init__(self):
        pass

    def create_sequence(self, N=1e7):
        expectedLength = N
        factor = int(expectedLength / 50.) #50 is the length of the small string hereafter
        subseq = "AGCTTTTCATTCTGACTGCAACGGGCAATATGTCAGTGTCTCGTTGCAAA"
        sequence = "".join([subseq]*factor)
        return sequence

