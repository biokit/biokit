import sys
import os
import glob
import inspect
import itertools

from converters import ConverterError, InvalidConverterError
from base import ConvBase


class Registry:

    def __init__(self):
        self._registry = {}
        self._fill_registry(os.path.normpath(os.path.dirname(__file__)))


    def _fill_registry(self, path):
        """
        Explore the directory converters to discover all converter classes
        (a concrete class which inherits from :class:`ConvBase`)
        and fill the register with the all input extensions, output extensions associated to this converter

        :param str path: the path of a directory to explore (not recursive)
        """
        def is_converter(item):
            obj_name, obj = item
            if not inspect.isclass(obj):
                return False
            return issubclass(obj, ConvBase) and not inspect.isabstract(obj)

        sys.path.insert(0, path)
        for f in glob.glob(os.path.join(path, '*.py')):
            module_name = os.path.splitext(os.path.basename(f))[0]
            if module_name not in ('__init__', 'base', 'registry'):
                try:
                    module = __import__(module_name, globals(), locals(), [module_name])
                except (ImportError, InvalidConverterError) as err:
                    print(">>> WARNING skip module '{}': {} <<<".format(module_name, err, file=sys.stderr))
                    continue
                converters = inspect.getmembers(module)
                converters = [c for c in converters if is_converter(c)]
                for converter_name, converter in converters:
                    print("### converter_name", converter_name, "converter", converter)
                    if converter is not None:
                        all_conv_path = itertools.product(converter.input_ext, converter.output_ext)
                        for conv_path in all_conv_path:
                            self[conv_path] = converter
        #clean the sys.path to avoid name collision
        sys.path.pop(0)


    def __setitem__(self, conv_path, value):
        """
        Set new
        :param conv_path: the input extension, the output extension
        :type conv_path: tuple of 2 strings
        :param value: the convertor which handle the conversion from input_ext -> output_ext
        :type value: :class:`ConvBase` object
        """
        if conv_path in self._registry:
            raise ConverterError('an other converter already exist for {} -> {}'.format(*conv_path))
        self._registry[conv_path] = value


    def __getitem__(self, conv_path):
        """

        :param conv_path: the input extension, the output extension
        :type conv_path: tuple of 2 strings
        :return: an object of subclass o :class:`ConvBase`
        """
        return self._registry[conv_path]


    def __contains__(self, conv_path):
        """
        can use membership operation on registry

        :param conv_path: the input extension, the output extension
        :type conv_path: tuple of 2 strings
        :return: True if conv_path is in registry otherwise False.
        """
        return conv_path in self._registry


    def __iter__(self):
        """
        make registry iterable through conv_path (str input extension, str output extension)
        """
        for path in self._registry:
            yield path