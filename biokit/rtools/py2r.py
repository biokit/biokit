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
from easydev import check_param_in_list


class Py2R(object):
    """Simple class to convert Python object to R objects as strings"""
    @staticmethod
    def from_bool(self, value):
        check_param_in_list(value, [True, False])
        if value is True:
            return "T"
        if value is False:
            return "F"

    def from_dict(self, value):
        return('list(' + ','.join(['%s=%s' % (self.Str4R(a[0]), self.Str4R(a[1])) 
            for a in value.items()]) + ')')

    def Str4R(self, obj):
        """convert a Python basic object into an R object in the form of string."""
        #return str_func.get(type(obj), OtherStr)(obj)
        # for objects known by PypeR
        if type(obj) in str_func:
            return(str_func[type(obj)](obj))

        # for objects derived from basic data types
        for tp in base_tps:
            if isinstance(obj, tp):
                return(str_func[tp](obj))
        # for any other objects
        return(OtherStr(obj))


