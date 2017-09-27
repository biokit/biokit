from easydev import TempFile, md5

from biokit import biokit_data
from biokit.converters.fasta2phylip import fasta2phylip


def test_conv():
    infile = biokit_data("converters/fa2phy.fasta")
    outfile = biokit_data("converters/fa2phy_desired_output.phylip")
    with TempFile(suffix=".phylip") as tempfile:
        convert = fasta2phylip(infile, tempfile.name)
        convert()

        # Check that the output is correct with a checksum
        assert md5(tempfile.name) == md5(outfile)
