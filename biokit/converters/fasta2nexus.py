from Bio import AlignIO


class Fasta2Nexus(object):
    """
    """
    def __init__(self, infile, outfile, *args, **kwargs):
        """
        """
        self.infile = infile
        self.outfile = outfile

    def __call__(self):

        input_handle = open(self.infile, "rU")
        output_handle = open(self.outfile, "w")

        alignments = AlignIO.parse(input_handle, "fasta")
        AlignIO.write(alignments, output_handle, "nexus")

        output_handle.close()
        input_handle.close()

