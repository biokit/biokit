import logging
from Bio import SeqIO

from .base import ConvBase


class Fastq2Fasta(ConvBase):
    """
    Convert :term:`FASTQ` to :term:`FASTA`
    """

    input_ext = ['.fastq', '.fq']
    output_ext = '.fasta'


    def __init__(self, inputfile, outputfile):
        """
        :param str infile: The path to the input FASTA file. 
        :param str outfile: The path to the output file
        """
        self.inputfile = inputfile
        self.outputfile = outputfile


    def __call__(self):
        """
        do the conversion  sorted :term`BAM` -> :term:'BED`
        the output will be stored in outputfile attribute

        :rtype: None 
        """
        records = SeqIO.parse(self.inputfile, 'fastq')
        SeqIO.write(records, self.outputfile, 'fasta')
