from biokit.converters.base import ConvBase
from biokit.converters.bam2bed import Bam2Bed
from biokit import biokit_data
from easydev import TempFile



def test_convbase():
    infile = biokit_data("converters/measles.fa")

    with TempFile(suffix=".bed") as outfile:
        Bam2Bed(infile, outfile.name)


    # Wrong name
    try:
        class TEST(ConvBase):
            input_ext = ".fa"
            output_ext = ".fq"
            def __call__(self):
                pass
        assert False
    except:
        assert True

    # add dot  
    class in2out(ConvBase):
        input_ext = "in"
        output_ext = "out"
        def __call__(self):
            pass

    # wrong input extension (int)
    try:
        class int2out(ConvBase):
            input_ext = [1]
            output_ext = ".out"
            def __call__(self):
                pass
        assert False
    except:
        assert True

    # add dot  mix case
    class in2out(ConvBase):
        input_ext = ["in", ".in2"]
        output_ext = "out"
        def __call__(self):
            pass

    try:
        class in2out(ConvBase):
            input_ext = 1
            output_ext = 2
            def __call__(self):
                pass
        assert False
    except:
        assert True

    class in2out(ConvBase):
        input_ext = [".fa"]
        output_ext = [".fq"]
        def __call__(self):
            self.execute("ls")
    this = in2out("test.fa", "test.fq")
    assert this.name== "in2out"
    this()


