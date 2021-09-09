# -*- python -*-
#
#  This file is part of biokit software
#
#  Copyright (c) 2014-
#
#  File author(s): Thomas Cokelaer <cokelaer@ebi.ac.uk>
#
#  Distributed under the GPLv3 License.
#  See accompanying file LICENSE.txt or copy at
#      http://www.gnu.org/licenses/gpl-3.0.html
#
#  website: https://github.com/biokit
#
##############################################################################
import sys
from types import *

from easydev import check_param_in_list

import pandas
import numpy


__all__ = [
    "BoolStr",
    "ReprStr",
    "FloatStr",
    "LongStr",
    "ComplexStr",
    "UniStr",
    "ByteStr",
    "SeqStr",
    "getVec",
    "NumpyNdarrayStr",
    "PandasDataFrameStr",
    "PandasSerieStr",
    "OtherStr",
    "Str4R",
]


if sys.version < "3.0":
    _mystr = _mybytes = lambda s: s
    _in_py3 = False
else:
    from functools import reduce

    long, basestring, unicode = int, str, str
    _mybytes = lambda s: bytes(s, "utf8")  # 'ascii')
    _mystr = lambda s: str(s, "utf8")
    _in_py3 = True


def BoolStr(obj):
    return obj and "TRUE" or "FALSE"


def ReprStr(obj):
    return repr(obj)


def FloatStr(f):
    if f is numpy.NaN or f is numpy.nan:
        return "NaN"  # or 'NA'
    if pandas.isnull(f):
        return "NaN"
    if numpy.isposinf(f):
        return "Inf"
    if numpy.isneginf(f):
        return "-Inf"
    return repr(f)


def LongStr(obj):
    rv = repr(obj)
    if rv[-1] == "L":
        rv = rv[:-1]
    return rv


def ComplexStr(obj):
    return repr(obj).replace("j", "i")


def UniStr(obj):
    return repr(obj.encode("utf8"))


def ByteStr(obj):
    return repr(obj)[1:]
    # return obj.decode()


def SeqStr(obj, head="c(", tail=")", enclose=True):
    if not enclose:  # don't add head and tail
        return ",".join(map(Str4R, obj))
    if not obj:
        return head + tail
    # detect types
    if isinstance(obj, set):
        obj = list(obj)
    obj0 = obj[0]
    tp0 = type(obj0)
    simple_types = [str, bool, int, long, float, complex]
    num_types = [int, long, float, complex]
    is_int = tp0 in (
        int,
        long,
    )  # token for explicit converstion to integer in R since R treat an integer from stdin as double
    if tp0 not in simple_types:
        head = "list("
    else:
        tps = (
            isinstance(obj0, basestring)
            and [StringType]
            or isinstance(obj0, bool)
            and [BooleanType]
            or num_types
        )
        for i in obj[1:]:
            tp = type(i)
            if tp not in tps:
                head = "list("
                is_int = False
                break
            elif is_int and tp not in (int, long):
                is_int = False
    # convert
    return (
        (is_int and "as.integer(" or "")
        + head
        + ",".join(map(Str4R, obj))
        + tail
        + (is_int and ")" or "")
    )


def DictStr(obj):
    return (
        "list("
        + ",".join(["%s=%s" % (Str4R(a[0]), Str4R(a[1])) for a in obj.items()])
        + ")"
    )


# 'b':boo
# lean, 'i':integer, 'u':unsigned int, 'f':float, c complex-float
# 'S'/'a':string, 'U':unicode, 'V':raw data. 'O':string?
_tpdic = {
    "i": "as.integer(c(%s))",
    "u": "as.integer(c(%s))",
    "f": "as.double(c(%s))",
    "c": "as.complex(c(%s))",
    "b": "c(%s)",
    "S": "c(%s)",
    "a": "c(%s)",
    "U": "c(%s)",
    "V": "list(%s)",
    "O": "as.character(c(%s))",
}


def getVec(ary):
    # used for objects from numpy and pandas
    tp = ary.dtype.kind
    if len(ary.shape) > 1:
        ary = ary.reshape(reduce(lambda a, b=1: a * b, ary.shape))
    ary = ary.tolist()
    if tp != "V":
        return _tpdic.get(tp, "c(%s)") % SeqStr(ary, enclose=False)
    # record array
    ary = list(map(SeqStr, ary))  # each record will be mapped to vector or list
    # use str here instead of repr since it has already been converted to str by SeqStr
    return _tpdic.get(tp, "list(%s)") % (", ".join(ary))


def NumpyNdarrayStr(obj):
    shp = obj.shape
    if len(shp) == 1:  # to vector
        tp = obj.dtype
        if tp.kind != "V":
            return getVec(obj)
        # One-dimension record array will be converted to data.frame
        def mapField(f):
            ary = obj[f]
            tp = ary.dtype.kind
            return '"%s"=%s' % (
                f,
                _tpdic.get(tp, "list(%s)") % SeqStr(ary.tolist(), enclose=False),
            )

        return "data.frame(%s)" % (", ".join(map(mapField, tp.names)))
    elif len(shp) == 2:  # two-dimenstion array will be converted to matrix
        return "matrix(%s, nrow=%d, byrow=TRUE)" % (getVec(obj), shp[0])
    else:  # to array
        dim = list(shp[-2:])  # row, col
        dim.extend(shp[-3::-1])
        newaxis = list(range(len(shp)))
        newaxis[-2:] = [len(shp) - 1, len(shp) - 2]
        return "array(%s, dim=c(%s))" % (
            getVec(obj.transpose(newaxis)),
            repr(dim)[1:-1],
        )


def PandasSerieStr(obj):
    return "data.frame(%s=%s, row.names=%s)" % (
        obj.name,
        getVec(obj.values),
        getVec(obj.index),
    )


def PandasDataFrameStr(obj):
    # DataFrame will be converted to data.frame, have to explicitly name columns
    # return 'data.frame(%s, row.names=%s)' % (', '.join(map(lambda a,b=obj:a+'='+getVec(obj[a]), obj)), getVec(obj.index))
    s = ", ".join(map(lambda a, b=obj: '"%s"=%s' % (str(a), getVec(obj[a])), obj))
    return "data.frame(%srow.names=%s)" % (s and s + ", ", getVec(obj.index))
    s = ""
    for col in obj:
        s = s + col + "=" + getVec(obj[col]) + ", "
    # print 'data.frame(%s row.names=%s)' % (s, getVec(obj.index))
    return "data.frame(%s row.names=%s)" % (s, getVec(obj.index))


def OtherStr(obj):
    if hasattr(obj, "__iter__"):  # for iterators
        if hasattr(obj, "__len__") and len(obj) <= 10000:
            return SeqStr(list(obj))
        else:  # waiting for better solution for huge-size containers
            return SeqStr(list(obj))
    return repr(obj)


str_func = {
    type(None): "NULL",
    bool: BoolStr,
    long: LongStr,
    int: repr,
    float: FloatStr,
    complex: ComplexStr,
    unicode: UniStr,
    str: repr,
    list: SeqStr,
    tuple: SeqStr,
    set: SeqStr,
    frozenset: SeqStr,
    dict: DictStr,
}  # str will override uncode in Python 3

base_tps = [
    type(None),
    bool,
    int,
    long,
    float,
    complex,
    str,
    unicode,
    list,
    tuple,
    set,
    frozenset,
    dict,
]  # use type(None) instead of NoneType since
# the latter cannot be found in the types module in Python 3

str_func[numpy.ndarray] = NumpyNdarrayStr
base_tps.append(numpy.ndarray)

str_func.update({pandas.Series: PandasSerieStr, pandas.DataFrame: PandasDataFrameStr})
base_tps.extend([pandas.Series, pandas.DataFrame])
base_tps.reverse()

if _in_py3:
    base_tps.append(bytes)
    str_func[bytes] = ByteStr


def Str4R(obj):
    """
    convert a Python basic object into an R object in the form of string.
    """
    # for objects known by PypeR
    if type(obj) in str_func:
        return str_func[type(obj)](obj)
    # for objects derived from basic data types
    for tp in base_tps:
        if isinstance(obj, tp):
            return str_func[tp](obj)
    # for any other objects
    return OtherStr(obj)
