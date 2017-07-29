"""Convert :term:`SAM` file to :term:`BAM` file"""
from biokit.converters.convbase import ConvBase


class BAM2SAM(ConvBase):
    """

    """
    def __init__(self, infile, outfile, *args, **kargs):
        """.. rubric:: constructor

        :param str infile:
        :param str outfile:

        command used::

            samtools view -Sbh
        """
        super(BAM2SAM, self).__init__(infile, outfile, *args, **kargs)

    def convert(self):
        # -S means ignored (input format is auto-detected)
        # -h means include header in SAM output
        #import pysam
        #pysam.sort("-o", self.infile, self.outfile)
        cmd = "samtools view -Sh {} -O SAM -o {}".format(self.infile, self.outfile)
        self.execute(cmd)



