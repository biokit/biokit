# -*- coding: utf-8 -*-
#
#  This file is part of Sequana software
#
#  Copyright (c) 2016 - Sequana Development Team
#
#  File author(s):
#      Thomas Cokelaer <thomas.cokelaer@pasteur.fr>
#      Dimitri Desvillechabrol <dimitri.desvillechabrol@pasteur.fr>,
#          <d.desvillechabrol@gmail.com>
#
#  Distributed under the terms of the 3-clause BSD license.
#  The full license is in the LICENSE file, distributed with this software.
#
#  website: https://github.com/biokit/biokit
#  documentation: http://biokit.readthedocs.io
#
##############################################################################
""".. rubric:: Standalone application dedicated to coverage"""
import os
import shutil
import glob
import sys
import argparse
from optparse import OptionParser
from argparse import RawTextHelpFormatter

from biokit import logger
from biokit.converters.utils import get_format_mapper

class Options(argparse.ArgumentParser):
    def  __init__(self, prog="converter"):
        usage = """\nTODO"""

        epilog = """ ----    """

        description = """DESCRIPTION:
        """

        super(Options, self).__init__(usage=usage, prog=prog,
                description=description, epilog=epilog)

        # options to fill the config file
        group = self.add_argument_group("Required argument")
        group.add_argument("-f", "--formats", dest="format", 
            action="store_true", default=False,
            help=("List available format ."))


def main(args=None):
    mapper = get_format_mapper()

    if args is None:
        args = sys.argv[:]

    user_options = Options(prog="converter")

    # If --help or no options provided, show the help
    if " -f" in args or " --format" in args:
        options = user_options.parse_args(args[1:])
        if options.format:
            print("Available mapping:")
            print("==================")
            for k in sorted(mapper):
                print("{}: {}".format(k, mapper[k]))
            sys.exit(0)

    if len(args) < 3:
        user_options.parse_args(["prog", "--help"])
    else:
        infile = args[1]
        outfile = args[2]
        options = user_options.parse_args(args[3:])

    inext = os.path.splitext(infile)[-1][1:]
    outext = os.path.splitext(outfile)[-1][1:]


    print(inext, outext)
    print(mapper)
    # Scanner les modules
    # get the names in lower case
    # Selectionner la classe en fonction des extensions 


    if inext not in mapper.keys():
        logger.critical("Input format not available in converters")
        logger.critical("Use --formats")
        sys.exit(1)

    if outext not in mapper[inext]:
        logger.critical("Output format not available in converters")
        logger.critical("Use --formats")
        sys.exit(1)

    # TODO dynamic inclusion of the class and module.
    import importlib
    importlib.import_module("biokit.converters.{}".format(inext + "2" + outext))

    if infile.endswith(".fastq"):
        if outfile.endswith(".fasta"):
            try:
                from biokit.converters.fastq2fasta import Fastq2Fasta
                convert = Fastq2Fasta(infile, outfile)
                convert()
            except:
                raise NotImplementedError
    elif infile.endswith(".bam"):
        if outfile.endswith(".bed"):
            from biokit.converters.bam2bed import Bam2Bed
            convert = Bam2Bed(infile, outfile)
            convert()
    else:
        print("converter not available")



if __name__ == "__main__":
   import sys
   main()#sys.argv)

