from biokit.rtools import session
import numpy as np
import os
import pytest
skiptravis = pytest.mark.skipif( "TRAVIS_PYTHON_VERSION" in os.environ,
    reason="On travis")


@skiptravis
def test_types():
    rs = session.RSession()
    rs.run("mylist = c(1,2)")
    assert all(rs.mylist == np.array([1,2]))

    rs.run("mybool = TRUE")
    assert rs.mybool is True

    rs.run("mystr = 'this'")
    assert rs.mystr == "this"

    rs.run("myint = 1")
    assert rs.myint == 1

    rs.run("myfloat = 1.2")
    assert rs.myfloat == 1.2

    rs.run("mynone = NA")
    assert rs.mynone is None

    rs.run("mynan = NaN")
    assert rs.mynan is np.nan

    rs.run("mynan = Inf")
    assert rs.mynan is np.inf


    # "ReprStr", "FloatStr", "LongStr", "ComplexStr", "UniStr",
    #"ByteStr", "SeqStr", "getVec", "NumpyNdarrayStr", 
    #"PandasSerieStr", "OtherStr", "Str4R" ]

