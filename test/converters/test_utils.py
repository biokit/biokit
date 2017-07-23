from biokit.converters import utils


def test_utils():


    res = utils.MapperRegistry()
    assert len(res)
    assert "bam2bed" in res
