from biokit import RNA


def test_rna():
    s1 = RNA('ACGU')
    s2 = RNA('AAAA')
    s1+s2
    s1+=s2

    assert len(s1) == 8
    assert s1._data == 'ACGUAAAA'


    s1.get_complement()
    s1.complement

    s1.get_reverse_complement()
    
    s1.gc_content()
    s1.get_dna()

    empty = RNA()
    empty.gc_content()
