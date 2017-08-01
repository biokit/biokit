from biokit.converters.bam2fasta import BAM2Fasta
from biokit import biokit_data
from easydev import TempFile, md5

def test_conv():
    infile = biokit_data("converters/measles.sorted.bam")
    outfile = biokit_data("converters/R1R2_from_bam.fasta")
    with TempFile(suffix=".fasta") as tempfile:
        convert = BAM2Fastq(infile, tempfile.name)
        convert()

        # Check that the output is correct with a checksum
        # Note that we cannot test the md5 on a gzip file but only
        # on the original data. This check sum was computed
        # fro the unzipped version of biokit/data/converters/measles.bed
        assert md5(tempfile.name) == md5(outfile)
