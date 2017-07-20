import logging

from Bio import SeqIO

class Fastq2Fasta(object):
    """
    Converts fastq to fasta
    """

    def __init__(self, inputfile, outputfile):
        self.inputfile = inputfile
        self.outputfile = outputfile

    def __call__(self):
        records = SeqIO.parse(self.inputfile, 'fastq')
        SeqIO.write(records, self.outputfile, 'fasta')