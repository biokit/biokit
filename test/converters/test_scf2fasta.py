from biokit.converters.scf2fasta import Scf2Fasta
from biokit import biokit_data
from easydev import TempFile, md5

def test_conv():
    # Scf V2 file
    infile_v2 = biokit_data("converters/sample_v2.scf")
    expected_outfile_v2 = biokit_data("converters/sample_v2.fasta")
    # Scf V3 file
    infile_v3 = biokit_data("converters/sample_v3.scf")
    expected_outfile_v3 = biokit_data("converters/sample_v3.fasta")

    with TempFile(suffix=".fasta") as tempfile:
        convert = Scf2Fasta(infile_v2, tempfile.name)
        convert()
        # Check that the output is correct with a checksum
        assert md5(tempfile.name) == md5(expected_outfile_v2)

        convert = Scf2Fasta(infile_v3, tempfile.name)
        convert()
        # Check that the output is correct with a checksum
        assert md5(tempfile.name) == md5(expected_outfile_v3)
