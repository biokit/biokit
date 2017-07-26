import logging
import os

from Bio import SeqIO


def generate_outfile_name(infile, out_extension):
    """
    Replaces the file extension with the given one.
    :param infile: Input file
    :param out_extension: Desired extension
    :return: The filepath with the given extension
    """
    return '%s.%s' % (os.path.splitext(infile)[0], out_extension)


class FASTA2PHYLIP(object):
    """
    Converts an alignment from Fasta format to Phylip.
    """

    def __init__(self, infile, outfile=None, alphabet=None, *args, **kwargs):
        self.fasta = infile
        self.phylip = outfile if outfile else generate_outfile_name(infile, 'phylip')
        self.alphabet = alphabet

    def __call__(self):
        sequences = list(SeqIO.parse(self.fasta, "fasta", alphabet=self.alphabet))
        count = SeqIO.write(sequences, self.phylip, "phylip")
        logging.debug("Converted %d records to phylip" % count)

