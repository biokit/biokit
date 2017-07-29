"""Convert :term:`BAM` file to :term:`fastq` file"""
from biokit.converters.convbase import ConvBase
import pysam


class BAM2Fastq(ConvBase):
    """Converts BAM 2 FastQ file

    .. warning:: the R1 and R2 reads are saved in the same file. Besides,
        there is no check that the read R1 and R2 alternates

    """
    def __init__(self, infile, outfile, *args, **kargs):
        """.. rubric:: constructor

        :param str infile:
        :param str outfile:

        library used::

            pysam (samtools)

        """
        super(BAM2Fastq, self).__init__(infile, outfile, *args, **kargs)

    def convert(self):
        # -S means ignored (input format is auto-detected)
        # -b means output to BAM format
        # -h means include header in SAM output
        pysam.bam2fq(self.infile, save_stdout=self.outfile)
