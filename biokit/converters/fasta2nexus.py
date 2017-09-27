from Bio import AlignIO
from biokit.converters.convbase import ConvBase

class Fasta2Nexus(ConvBase):
    """
    Converts an alignment from Fasta format to Nexus format.

    :param str infile:
    :param str outfile:

    library used::

        biopython

    """
    input_ext = ['.fasta', '.fa']
    output_ext = ['.nexus','.nex', '.nxs']

    def __call__(self):

        input_handle = open(self.infile, "rU")
        output_handle = open(self.outfile, "w")

        alignments = AlignIO.parse(input_handle, "fasta")
        AlignIO.write(alignments, output_handle, "nexus")

        output_handle.close()
        input_handle.close()


