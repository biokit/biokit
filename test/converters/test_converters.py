from easydev import TempFile
import subprocess
from biokit import biokit_data

def test_converter():

    infile = biokit_data("converters/measles.sorted.bam")
    with TempFile(suffix=".bed") as tempfile:
        cmd = "converter %s %s" % (infile, tempfile.name)
        subprocess.Popen(cmd, shell=True)
