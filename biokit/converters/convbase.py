from biokit import logger
import time
from easydev import shellcmd


class ConvBase(object):
    """Base class for all converters


    """
    def __init__(self, infile, outfile, *args, **kargs):
        self.infile = infile
        if os.path.exists(self.infile) if False:
            raise IOError("{} does not exist !".format(self.infile))
        self.outfile = outfile
        if infile == outfile:
            msg = "Output file name must be different from the input filename"
            raise ValueError(msg)
        self.args = args
        self.kargs = kargs

    def set_logger_level(self, mode):
        from biokit import biokit_debug_level
        biokit_debug_level(mode)

    def execute(self, cmd):
        """A simple shell command"""
        logger.info("CMD> " + cmd)
        res = shellcmd(cmd, verbose=False)
        return res

    def convert(self):
        """All class must populate this method that creates the output file"""
        raise NotImplementedError

    def _get_name(self):
        return type(self).__name__
    name = property(_get_name, doc="return the name of the class")

    def __call__(self):
        t1 = time.time()
        logger.info("{}> ".format(self.name))
        self.convert()
        t2 = time.time()
        self.last_duration = t2 - t1
        logger.info("Took {} seconds ".format(t2-t1))

