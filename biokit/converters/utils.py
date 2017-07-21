import inspect
import biokit
from biokit import converters
import pkgutil
import importlib
import collections

def get_format_mapper():
    """This functions returns a dictionary with authorised mapper

    The dictionary is built dynamically assuming that there is only
    one class to be found in the modules provides in biokit.converters


    """
    mapper = collections.defaultdict(list)

    # First, let us figure out the modules of interest.
    modules = pkgutil.iter_modules(biokit.converters.__path__)
    for module in modules:
        modulename = module[1]

        importlib.import_module("biokit.converters." + modulename)

        classes = inspect.getmembers(getattr(biokit.converters, modulename),
                                     inspect.isclass)

        # Here, we must have only 2 classes: the Bam2Bed if the module is called
        # bam2bed and the ConvBase 
        classname = [this for this in classes if this[0] != "ConvBase"]


        if len(classname) >0:
            name = classname[0][0]
            k, v = name.lower().split("2")
            mapper[k].append(v)
    return mapper
