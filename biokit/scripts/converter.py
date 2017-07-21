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
        group.add_argument("-i", "--input", dest="input", type=str,
            help=("Input file in BED or BAM format. If a BAM file is "
                 "provided, it will be converted locally to a BED file "
                 "using genomecov, which must be installed."))

def main(args=None):

    if args is None:
        args = sys.argv[:]

    user_options = Options(prog="converter")

    # If --help or no options provided, show the help
    if len(args) < 3:
        user_options.parse_args(["prog", "--help"])
    else:
        infile = args[1]
        outfile = args[2]
        options = user_options.parse_args(args[3:])

    inext = os.path.splitext(infile)[1]
    outext = os.path.splitext(outfile)[1]


    # Scanner les modules
    # get the names in lower case
    # Selectionner la classe en fonction des extensions 


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

