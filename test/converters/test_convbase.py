from biokit.converters.convbase import ConvBase
from biokit import biokit_data
from easydev import TempFile



def test_convbase():
    infile = biokit_data("converters/measles.fa")
    try:
        cb = ConvBase(infile, infile)
        assert False
    except ValueError:
        assert True
    except:
        assert False

    with TempFile() as outfile:
        cb = ConvBase(infile, outfile.name)
        cb.set_logger_level("DEBUG")
        try:
            cb.convert()
            assert False
        except NotImplementedError:
            assert True


    with TempFile() as outfile:
        try:
            cb = ConvBase("dummy", outfile.name)
            assert False
        except IOError:
            assert True
        except:
            assert False
            
