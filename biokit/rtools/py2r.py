from easydev import check_params_in_list









class Py2R(object):

    @staticmethod
    def from_bool(self, value):
        check_params_in_list(value, [True, False]
         if value is True:
            return "T"
         if value is False:
            return "F"

    def from_dict(self, value):
        return('list(' + ','.join(['%s=%s' % (Str4R(a[0]), Str4R(a[1])) 
            for a in value.items()]) + ')')

    def Str4R(obj):
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


