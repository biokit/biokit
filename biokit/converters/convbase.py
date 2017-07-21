from biokit import logger
import time
from easydev import shellcmd







class ConvBase(object):
    def __init__(self, infile, outfile, *args, **kargs):
        self.infile = infile
        self.outfile = outfile
        self.args = args
        self.kargs = kargs

    def set_logger_level(self, mode):
        from biokit import biokit_debug_level
        biokit_debug_level(mode)

    def execute(self, cmd):
        logger.info("CMD> " + cmd)
        res = shellcmd(cmd, verbose=False)
        return res

    def convert(self):
        raise NotImplementedError

    def _get_name(self):
        return type(self).__name__
    name = property(_get_name)

    def __call__(self):
        t1 = time.time()
        logger.info("{}> ".format(self.name))
        self.convert()
        t2 = time.time()
        self.last_duration = t2 - t1
        logger.info("Took {} seconds ".format(t2-t1))

