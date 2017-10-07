"""Convert :term:`BAM` file to :term:`fastq` file"""
from biokit.converters.base import ConvBase
import pysam


class BAM2Fastq(ConvBase):
    """Converts BAM 2 FastQ file

    .. warning:: the R1 and R2 reads are saved in the same file. Besides,
        there is no check that the read R1 and R2 alternates

    """
    input_ext = [".bam"]
    output_ext = [".fastq", ".fq"]
    def __init__(self, infile, outfile, *args, **kargs):
        """.. rubric:: constructor

        :param str infile:
        :param str outfile:

        library used::

            pysam (samtools)

        """
        super(BAM2Fastq, self).__init__(infile, outfile, *args, **kargs)

    def __call__(self):
        # This fails with unknown error
        #pysam.bam2fq(self.infile, save_stdout=self.outfile)

        #cmd = "samtools fastq %s >%s" % (self.infile, self.outfile)
        #self.execute(cmd)

        # !!!!!!!!!!!!!!!!!! pysam.bam2fq, samtools fastq and bamtools convert
        # give differnt answers...

        cmd = "bamtools convert -format fastq -in {0} -out {1}".format(
            self.infile, self.outfile
        )
        self.execute(cmd)
