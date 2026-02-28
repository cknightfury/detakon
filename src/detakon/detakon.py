import json
from pathlib import Path
from io import IOBase, TextIOWrapper
from types import GeneratorType
from csv import DictReader, DictWriter

class Detakon():
    """detakon uses a detakon map to convert data."""
    def __init__(self, detamap, source, destination, *args, **kargs):
        """
        Initialize all values for Detakon object.
        
        :param self: Object reference.
        :param detamap: detamap location that describes field mappings, default values, and operations to perform on data.
        :param source: Source to input.  See load_source method for accepted types.
        :param destination: Destination to output.
        :param args: Additional parameters.
        :param kargs: Addtional flags.
        """
        self.detamap: dict = self.load_detamap(detamap)
        self.mappings: dict = self.detamap["Mappings"]
        self.source = source
        self.destination = destination
        data_generator = self.source_reader()
        output_info: dict = self.detamap["Output"]
        output = output_info["argument"]

        # branch to determine output method called based on detamap.Output.argument for destination parameter
        # filepath as either string or Path object 
        if output == "filepath":
            if output_info["type"] == "str":
                self.destination = Path(self.destination)

            # if not appending to existing file, delete if file exists and create new empty file
            if not output_info.get("append", False) and self.destination.exists() and self.destination.is_file():
                self.destination.unlink()

            if self.destination.exists() and self.destination.is_file():
                new_file = False
            else:
                new_file = True
            self.destination.touch()

            with self.destination.open(mode="a",
                        buffering=output_info.get("buffering", -1),
                        encoding=output_info.get("encoding", "utf-8"),
                        errors=output_info.get("errors", None),
                        newline=output_info.get("newline", None)) as file:
                csv_writer = DictWriter(file,
                            fieldnames=self.detamap["Fields"],
                            restval=output_info.get("restval", ""),
                            extrasaction=output_info.get("extrasaction", "raise"),
                            dialect=output_info.get("dialect", "excel"),
                            delimiter=output_info.get("delimiter", ","),
                            quotechar=output_info.get("quotechar", '"'),
                            escapechar=output_info.get("escapechar", None),
                            doublequote=output_info.get("doublequote", True),
                            skipinitialspace=output_info.get("skipinitialspace", False),
                            lineterminator=output_info.get("lineterminator", "\r\n"),
                            quoting=output_info.get("quoting", 0),
                            strict=output_info.get("strict", False))
                
                if new_file and not output_info.get("omit_heading", False):
                    csv_writer.writeheader()
                for entry in data_generator:
                    row_data = {}
                    for source_field, destination_field in self.mappings.items():
                        row_data[destination_field] = entry[source_field]
                    csv_writer.writerow(row_data)
        elif output == "return":
            pass

    def source_reader(self):
        """
        Validate source type, and return a generator object if possible, otherwise return full object in accepted format.

        Intent to add remote file, or result of API calls - giving consideration to add ability, or require calling application to submit data directly.
        
        :param self: Object reference.
        :param source: Source data.  File as string, Path object, or an opened file object.  Also can accept string object of CSV (comma or tab delimited), or JSON.
        :return: File path as string.
        :rtype: str
        """
        # get source information from detamap
        source_info: dict = self.detamap["Source"]

        # branch based on source.argument value provided in detamap

        # handler for source.argument being a filepath
        # filepath must be either a string to a file, or a Path object for a file.
        if source_info["argument"] == "filepath":
            if source_info["type"] == "str":
                self.source = Path(self.source)
            if self.source.exists() and self.source.is_file():
                with self.source.open(mode='r',
                                        buffering=source_info.get("buffering", -1),
                                        encoding=source_info.get("encoding", "utf-8"),
                                        errors=source_info.get("errors", None),
                                        newline=source_info.get("newline", None)) as source_file:
                    # handler for source.format csv values.  if no source.format value is provided, csv value is default
                    if source_info.get("format", "csv") == "csv":
                        # DictReader defaults are used if Source does not contain a key for a given keyword.
                        # key:value paris can be provided in the detamap Source section to set the value of any DictReader keyword.
                        # values must conform with DictReader's expectation.
                        csv_reader = DictReader(source_file,
                                                fieldnames=source_info.get("fieldnames", None),
                                                restkey=source_info.get("restkey", None),
                                                restval=source_info.get("restval", None),
                                                dialect=source_info.get("dialect", "excel"),
                                                delimiter=source_info.get("separator", ","),
                                                quotechar=source_info.get("quotechar", '"'),
                                                escapechar=source_info.get("escapechar", None),
                                                doublequote=source_info.get("doublequote", True),
                                                skipinitialspace=source_info.get("skipinitialspace", False),
                                                lineterminator=source_info.get("lineterminator", "\r\n"),
                                                quoting=source_info.get("quoting", 0),
                                                strict=source_info.get("strict", False))
                        for row in csv_reader:
                            yield row

        # elif isinstance(source, TextIOWrapper):
        #     pass
        # elif isinstance(source, str):
        #     if Path(source).exists() and Path(source).is_file():
        #         pass
        #     elif isinstance(source, dict):
        #         pass
        # elif isinstance(source, GeneratorType):
        #     pass
        # else:
        #     raise ValueError("Source could not be determined.")

    def load_detamap(self, detamap) -> dict:
        """
        Process object passed as detamap and return dictionary detamap.
        
        :param self: Object reference.
        :param detamap: Either a dictionary, JSON stream/string, or file path (string or pathlib.Path) to JSON file.
        :return: Dictionary of detamap
        :rtype: dict
        """
        # accepts python dictionary or JSON data.  Future plans to add TOML detamap.
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
        