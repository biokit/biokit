from biokit import DNA


def test_dna():
    s1 = DNA('ACGT')
    s2 = DNA('AAAA')
    s1+s2
    s1+=s2

    assert len(s1) == 8
    assert s1._data == 'ACGTAAAA'


    s1.get_complement()
    s1.complement

    s1.get_reverse_complement()
    
    s1.gc_content()
    s1.get_rna()

    empty = DNA()
    empty.gc_content()


