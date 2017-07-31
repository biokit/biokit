import abc


class ConvMeta(abc.ABCMeta):
    """
    This the metaclass control that the converter classes have the right characteristics

       * have an attribute input_ext
       * have an attribute output_ext

    It should not be used directly, it should be used through the :class:`ConvBase` class.
    The standard way to build a new converter is to inherits from :class:`ConvBase`
    or a subclasses of it, for instance: ::

        class Fasta_2_Fasta(ConvBase):

            input_ext = ['.fa', '.fst', '.fasta']
            output_ext = '.fa'

        __call__(self, *args, **kwargs):
            do conversion
    """

    def __init__(cls, name, bases, classdict):

        def check_ext(ext, io_name):
            """
            Check if extension is specified correctly.
            I must be a string or a sequence of string, otherwise raise an error
            it should start by a dot otherwise fix extension and inject it in the class

            :param ext: the value of the class attribute (input|output)_ext
            :param str io_name: the type of extension, 'input' or output'
            :raise TypeError:  if ext is neither a string nor a sequence of strings
            """
            if isinstance(ext, str):
                if not ext.startswith('.'):
                    ext = '.' + ext
                setattr(cls, '{}_ext'.format(io_name),  (ext, ))
            elif isinstance(ext, (list, tuple, set)):
                if not all([isinstance(ext, str) for ext in input_ext]):
                    raise TyepError("each element of the class attribute '{}.{}_ext' "
                                    "must be a string".format(cls, io_name))
                else:
                    if not all([ext.startswith('.') for ext in input_ext]):
                        all_ext = []
                        for one_ext in ext:
                            if one_ext.startswith('.'):
                                all_ext.append(one_ext)
                            else:
                                all_ext.append('.' + one_ext)
                    setattr(cls, '{}_ext'.format(io_name), all_ext)
            else:
                import sys
                err = "the class attribute '{}.{}_ext' must be specified in the class or subclasses".format(cls, io_name)
                print(">>> WARNING skip class '{}': {} <<<".format(cls.__name__, err, file=sys.stderr))
                raise TypeError("the class attribute '{}.{}_ext' must be specified "
                                "in the class or subclasses".format(cls, io_name))
            return True
        if not name == 'ConvBase':
            if '2' not in name:
                raise TypeError("converter name must follow convention inputformat2outputformat")
            input_fmt, output_fmt, *_ = name.upper().split('2')
            input_ext = getattr(cls, 'input_ext')
            if check_ext(input_ext, 'input'):
                output_ext = getattr(cls, 'output_ext')
                check_ext(output_ext, 'output')
            setattr(cls, 'input_fmt', input_fmt)
            setattr(cls, 'output_fmt', output_fmt)



class ConvBase(metaclass=ConvMeta):
    """
    This is the base class for all converters.
    To build a new converter create a new class which inherits of :class:`ConvBase`
    and implement __call__ method (which is abstract). The class attributes
    input_ext and output_ext must be also override in the subclass.
    for instance: ::

        class Fasta_2_Fasta(ConvBase):

            input_ext = ['.fa', '.fst', '.fasta']
            output_ext = '.fa'

        __call__(self, *args, **kwargs):
            do conversion
    """

    """specify the extensions of the input file, can be a sequence (must be overridden in subclasses)"""
    input_ext = None
    """specify the extensions of the output file, can be a sequence (must be overridden in subclasses)"""
    output_ext = None


    def __init__(self, infile, outfile):
        """

        :param str infile: The path of the input file.
        :param str outfile: The path of The output file
        """
        self.infile = infile
        self.outfile = outfile


    @abc.abstractmethod
    def __call__(self, *args, **kwargs):
        """
        must be override in subclasses
        """
        print('args=', args, 'kwargs=', kwargs)
