







class ConvBase(object):
    def __init__(self, infile, outfile, *args, **kargs):
        self.infile = infile
        self.outfile = outfile
        self.args = args
        self.kargs = kargs

    def execute(self, cmd):
        from easydev import shellcmd
        shellcmd(cmd)

