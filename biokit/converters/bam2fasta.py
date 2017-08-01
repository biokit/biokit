# coding: utf-8
"""Convert :term:`BAM` format to :term:`Fasta` format."""
from biokit.converters.convbase import ConvBase

__all__ = ["Bam2Fasta"]

class Bam2Fasta(ConvBase):
    """Bam2Fasta converter

    Wrapper of bamtools to convert bam file to fasta file.
    """
    def __init__(self, infile, outfile, *args, **kwargs):
        """.. rubric:: constructor

        :param str infile: input BAM file.
        :param str outfile: input Fasta file.
        """
        super(Bam2Fasta, self).__init__(infile, outfile, *args, **kwargs)

    def convert(self):
        cmd = "bamtools convert -format fasta -in {0} -out {1}".format(
            self.infile, self.outfile
        )
        self.execute(cmd)
