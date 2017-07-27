from biokit.converters.convbase import ConvBase





def test_convbase():
    cb = ConvBase("test.sam", "test.bam")
    try:
        cb = ConvBase("test.sam", "test.sam")
        assert False
    except ValueError:
        assert True
    except:
        assert False
