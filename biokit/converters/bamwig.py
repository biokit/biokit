from .base import ConvBase


class bam2wig(ConvBase):
    """bam2wig does not implement __call__ so it's still an abstract class
       so it not registered
    """
    input_ext = ['bam']
    output_ext = '.wig'

class wig2bam(ConvBase):
    """
    whereas wig2bam implement __call__ so it's a concrete class
    """
    input_ext = '.bam'
    output_ext = ['.wig', '.wog']

    def __call__(self, *args, **kwargs):
        print("I'm not abstract anymore")

 
