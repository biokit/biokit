from biokit import logger







class ConvBase(object):
    def __init__(self, infile, outfile, *args, **kargs):
        self.infile = infile
        self.outfile = outfile
        self.args = args
        self.kargs = kargs

    def execute(self, cmd):
        import time
        t1 = time.time()
        logger.info("CMD> " + cmd)
        from easydev import shellcmd
        res = shellcmd(cmd, verbose=False)
        t2 = time.time()
        self.last_duration = t2 - t1
        logger.info("Took {} seconds ".format(t2-t1))
        return res

    

