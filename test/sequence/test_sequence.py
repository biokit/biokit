from biokit import Sequence, DNA



def test():
    s1 = Sequence('ACGT')
    s2 = Sequence('AAAA')
    s1 + s2
    s2 + s1
    s1+= s2
    "aa" + s1

    try:
        s1 += 2
        assert False
    except:
        assert True

    s1.histogram()
    s1.pie() 

    d1 = Sequence('GAGCCTACTAACGGGAT')
    d2 = Sequence('CATCGTAATGACGGCCT')
    #d1 = Sequence(d2)
    assert d1.hamming_distance(d2) == 7
                   
    d1.lower()
    assert d1.sequence == 'gagcctactaacgggat'
    d2.upper()


    d1._check_sequence()

    # __repr__ and __str__
    print(d1)
    d1.__repr__()
    d1 = Sequence('AAAAa') # length greater than 10
    print(d1)
    d1.__repr__()


    d1 = Sequence('ACGT')
    dna = DNA('ACGT')
    try:
        d1 += rna
        assert False
    except:
        assert True
    try:
        dna += d1
        assert False
    except:
        assert True


    s = Sequence(DNA('ACGT'))
    assert s == 'ACGT'
    assert s == dna
