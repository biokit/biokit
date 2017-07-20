from biokit.converters.convbase import ConvBase





class Bam2Bed(ConvBase):
    """


    """
    def __init__(self, infile, outfile, *args, **kargs):
        """.. rubric:: constructor

        :param str filename
        """
        super(Bam2Bed, self).__init__(infile, outfile, *args, **kargs)
        pass

    def __call__(self):
        cmd = "samtools depth -aa {} > {}".format(self.infile, self.outfile)
        self.execute(cmd)



