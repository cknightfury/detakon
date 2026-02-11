import json
from pathlib import Path
from io import IOBase, TextIOWrapper
from types import GeneratorType

class Detakon():
    """detakon uses a detakon map to convert data."""
    def __init__(self, detamap, source, destination, sdtype: str="csv", ddtype: str="csv", *args, **kargs):
        """
        Initialize all values for Detakon object.
        
        :param self: Object reference.
        :param detamap: detamap location that describes field mappings, default values, and operations to perform on data.
        :param source: Source to input.  See load_source method for accepted types.
        :param destination: Destination to output.
        :param sdtype: Source data format type. Defaults to CSV.
        :type sdtype: str
        :param ddtype: Destination data format type. Defaults to CSV.
        :type ddtype: str
        :param args: Additional parameters.
        :param kargs: Addtional flags.
        """
        self.detamap = self.load_detamap(detamap)
        self.source = self.load_source(source) # see note in method pass

    def load_source(self, source) -> str:
        """
        Validate source type, and return a generator object if possible, otherwise return full object in accepted format.

        Intent to add remote file, or result of API calls - giving consideration to add ability, or require calling application to submit data directly.
        
        :param self: Object reference.
        :param source: Source data.  File as string, Path object, or an opened file object.  Also can accept string object of CSV (comma or tab delimited), or JSON.
        :return: File path as string.
        :rtype: str
        """
        # Thoughts: Accept file or generator object reference - rely on caller to supply data stream if not a file.
        # Halted development - reconsideration for how to additionally accept non-file streams
        if isinstance (source, Path):
            pass
        elif isinstance(source, TextIOWrapper):
            pass
        elif isinstance(source, str):
            if Path(source).exists() and Path(source).is_file():
                pass
        else:
            pass

    def load_detamap(self, detamap) -> dict:
        """
        Process object passed as detamap and return dictionary detamap.
        
        :param self: Object reference.
        :param detamap: Either a dictionary, JSON stream/string, or file path (string or pathlib.Path) to JSON file.
        :return: Dictionary of detamap
        :rtype: dict
        """
        if isinstance(detamap, dict):
            return detamap
        elif isinstance(detamap, str) and detamap[0] == '{':
            try:
                return json.loads(detamap)
            except Exception as e:
                raise Exception(f"Failed to load JSON string: {e}")
        else:
            try:
                if isinstance(detamap, Path):
                    with detamap.open("r") as file:
                        return json.load(file)
                else:
                    with open(detamap, "r") as file:
                        return json.load(file)
            except Exception as e:
                raise Exception(f"Failed to load JSON file: {e}")
        