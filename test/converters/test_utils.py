from biokit.converters import utils


def test_utils():


    res = utils.get_format_mapper()
    assert len(res)
    assert "bed" in res['bam']
