from biokit.converters.fastq2fasta import Fastq2Fasta
from biokit import biokit_data
from easydev import TempFile, md5


def test_conv():
    infile = biokit_data("converters/test_fastq_1.fastq")

    with TempFile(suffix=".fasta") as tempfile:
        convert = Fastq2Fasta(infile, tempfile.name)
        convert()

        print(md5(biokit_data("converters/test_fasta_1.fasta")))
        # Check that the output is correct with a checksum
        # Note that we cannot test the md5 on a gzip file but only 
        # on the original data. This check sum was computed
        # fro the unzipped version of biokit/data/converters/measles.bed
        #assert md5(tempfile.name) == "7ad97cfaec70785234e323457cb5599e"

        # RIGHT NOW? BIOPYTHON C§HANGES > into @ need to check

#test_conv()
