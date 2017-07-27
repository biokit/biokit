from biokit.converters.convbase import ConvBase


class SAM2CRAM(ConvBase):
    """

    """
    def __init__(self, infile, outfile, reference, *args, **kargs):
        """.. rubric:: constructor

        :param str filename

        command used::

            samtools view -SCh

        .. note:: the API related to the third argument may change in the future.
        """
        super(SAM2CRAM, self).__init__(infile, outfile, *args, **kargs)
        self.reference = reference

    def convert(self):
        # -S means ignored (input format is auto-detected)
        # -b means output to BAM format
        # -h means include header in SAM output
        cmd = "samtools view -SCh {} -T {} > {}".format(self.infile,
            self.reference, self.outfile)
        self.execute(cmd)



