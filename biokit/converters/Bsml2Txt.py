"""Convert :term:`BSML` format to :term:`TXT` formats"""
from biokit.converters.convbase import ConvBase
from libsbml import *

class Bsml2Txt(ConvBase):
    """
    """
    def __init__(self, infile, outfile, *args, **kargs):
        """.. rubric:: constructor
        :param str filename
        """
        self.infile = infile
        self.outfile = outfile
        
        super(Bsml2Txt, self).__init__(infile, outfile, *args, **kargs)

    def __call__(self):
        
        output_handle = open(self.outfile, "w")
        
        AlignIO.write(writeSBMLToString(SBMLReader(self.infile)), output_handle, "txt")
        
        output_handle.close()
