"""Convert :term:`BSML` format to :term:`TXT` formats"""
from biokit.converters.convbase import ConvBase
from libsbml import *


class SBML2txt(ConvBase):
    """
    """
    input_ext = ['sbml']
    output_ext = '.txt'

    def __call__(self):
        with open(self.outfile, "w") as output_handle:
            output_handle.write(writeSBMLToString(SBMLReader(self.infile)))
