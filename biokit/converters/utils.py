import inspect
from biokit import converters
import pkgutil
import importlib



class MapperRegistry(dict):

    def __init__(self):
        self.init()

    def init(self):
        """This functions returns a dictionary with authorised mapper

        The dictionary is built dynamically assuming that there is only
        one class to be found in the modules provides in biokit.converters

        """
        mapper = {}

        # First, let us figure out the modules of interest.
        modules = pkgutil.iter_modules(converters.__path__)
        for module in modules:
            modulename = module[1]

            importlib.import_module("biokit.converters." + modulename)

            classes = inspect.getmembers(getattr(converters, modulename),
                                     inspect.isclass)

            # Here, we must have only 2 classes: the Bam2Bed if the module is called
            # bam2bed and the ConvBase 
            classname = [this for this in classes if this[0] != "ConvBase"]

            if len(classname) >0:   
                name = classname[0][0]
                if "2" in name:
                    k, v = name.lower().split("2")
                    mapper[k + "2" + v] = name
        for k,v in mapper.items():
            self[k] = v

