
def _numgoid(value):
    if isinstance(value, str):
        # try to cast the value
        value = int(value)
    elif isinstance(value, int):
        pass
    else:
        raise TypeError("value must be a string or an integer")

    goId = "GO:%08d" % value
    assert len(goId) == 11, ValueError("Input number seems too large {}".format(value))

    return goId

def num2goid(numbers):
    """converts the numbers into Gene Ontology IDs. 

    :param list numbers: a list of integer or strings or just a string or int. The numbers must be 
    :return: list of GO Ids

    IDs are seven-digit numbers preceded by the prefix GO: (Gene Ontology database standard).

    """
    if isinstance(numbers, list):
        res = [_numgoid(x) for x in numbers]
    else:
        res = _numgoid(numbers)
    return res

