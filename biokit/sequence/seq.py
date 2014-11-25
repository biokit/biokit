
import ctypes
cseqkit = ctypes.CDLL("complement.so")
cseqkit.dna_complement.restype = ctypes.c_char_p
import string




class Seq(str):
    trans = string.maketrans('ACGTagct', 'TGCAtgca')
    def __init__(self, data=""):
        self.data = data
    def get_complement(self):
        return self.translate(self.trans)
    def count(self):
        pass

    def get_complement_c(self, sequence=None):
        if sequence:
            return cseqkit.dna_complement(sequence, len(sequence))
        else:
            return cseqkit.dna_complement(self.data, len(self.data))



    def get_complement_dict(self, by=2):
        pass
        




