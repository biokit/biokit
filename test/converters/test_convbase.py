from biokit.converters.convbase import ConvBase
from biokit import biokit_data




def test_convbase():
    infile = biokit_data("converters/measles.fa")
    try:
        cb = ConvBase(infile, infile)
        assert False
    except ValueError:
        assert True
    except:
        assert False
