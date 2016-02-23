from biokit.network.complexes import Complexes
from nose.plugins.attrib import attr



@attr("skiptravis")
def test_complexes():
    c = Complexes(cache=True)
    c.remove_homodimers()
    and_gates, subset = c.search_complexes(['P54289'])
    and_gates, subset = c.search_complexes(['P54289'], verbose=True)
    assert len(subset)


    c.search('P54289')
    c.hist_participants()
    c.stats()


    # let us find a complex with all its participants
    user_species = ['Q13936', u'Q08289', u'P54289']
    and_gates, subset = c.search_complexes(user_species)
    assert len(and_gates)
    assert 'EBI-9687812' in and_gates.keys()


    assert c.uniprot2genename('Q13936') == ['CACNA1C CACH2 CACN2 CACNL1A1 CCHL1A1']
    try:
        assert c.uniprot2genename('dummy')
        assert False
    except:
        assert True


    assert c.chebi2name('CHEBI:18420') == 'magnesium(2+)'
    

