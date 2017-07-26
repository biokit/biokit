from biokit.converters.convbase import ConvBase


class Sam2Bam(ConvBase):
    """


    """
    def __init__(self, infile, outfile, *args, **kargs):
        """.. rubric:: constructor

        :param str filename
        """
        super(Sam2Bam, self).__init__(infile, outfile, *args, **kargs)
        pass

    def __call__(self):
        cmd = "samtools view -Sbh {} > {}".format(self.infile, self.outfile)
        self.execute(cmd)



