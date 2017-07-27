"""Convert :term:`SAM` file to :term:`BAM` file"""
from biokit.converters.convbase import ConvBase


class SAM2BAM(ConvBase):
    """

    """
    def __init__(self, infile, outfile, *args, **kargs):
        """.. rubric:: constructor

        :param str infile:
        :param str outfile:

        command used::

            samtools view -Sbh
        """
        super(SAM2BAM, self).__init__(infile, outfile, *args, **kargs)

    def convert(self):
        # -S means ignored (input format is auto-detected)
        # -b means output to BAM format
        # -h means include header in SAM output
        cmd = "samtools view -Sbh {} > {}".format(self.infile, self.outfile)
        self.execute(cmd)



