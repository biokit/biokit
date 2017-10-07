from biokit.converters import utils


def _test_utils():


    res = utils.MapperRegistry()
    assert len(res)
    assert "bam2bed" in res
