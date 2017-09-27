"""Convert :term:`BSML` format to :term:`TXT` formats"""
from biokit.converters.convbase import ConvBase
from libsbml import *

class Bsml2Txt(ConvBase):
    
    """
    """
    input_ext = ['bsml']
    output_ext = '.txt'

    def __init__(self, infile, outfile):
        """.. rubric:: constructor
        :param str filename
        """
        self.infile = infile
        self.outfile = outfile
        
        super(Bsml2Txt, self).__init__(infile, outfile)
        
    def __call__(self):
        
        with open(self.outfile, "w") as output_handle:
        
            output_handle.write(writeSBMLToString(SBMLReader(self.infile)))
