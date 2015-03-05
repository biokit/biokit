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
from .session import RSession

__all__ = ["bool2R", "rcode"]


def bool2R(value):
    """Transforms a boolean into a R boolean value T or F"""
    if value is True:
        return "T"
    if value is False:
        return "F"
    else:
        raise ValueError("expecting a boolean value")


def rcode(code, verbose=True):
    """Run a R script and return the RSession object"""
    r = RSession(verbose=verbose)
    r.run(code)
    return r




