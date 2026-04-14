import json
from pathlib import Path
from io import IOBase, TextIOWrapper
from types import GeneratorType
from csv import DictReader, DictWriter
from operator import methodcaller
from decimal import Decimal
from collections.abc import Generator

class Detakon():
    """detakon uses a detakon map to convert data."""
    def __init__(self, detamap, source, destination, *args, **kargs):
        """
        Initialize all values for Detakon object.
        
        :param self: Object reference.
        :param detamap: detamap location or dictionary that describes field mappings, default values, and operations to perform on data.
        :param source: Source to input.  See load_source method for accepted types.
        :param destination: Destination to output.
        :param args: Additional parameters.
        :param kargs: Addtional flags.
        """
        self.original_detamap = detamap
        self.set_detamap() # set detamap member variables, and member variables for each sub-map: mappings, defaults, operations, source_info, _output_info, etc
        self.source = source
        self.destination = destination

    def set_detamap(self, detamap=None) -> None:
        """
        For interactive sessions to change the detamap. Pass new detamap as argument.
        
        If no argument is provided, the original detamap will be reloaded; if the original detamap was a file, this will update the with any changes from the file.
        
        :param detamap: New detamap.  Default to reloading self.original_detamap (which is stored during __init__)."""
        self.detamap: dict = self._load_detamap(self.original_detamap) if detamap is None else self._load_detamap(detamap)
        self.lang: dict = self._load_language(self.detamap.get("lang", "en-us"))
        self.mappings: dict = self.detamap[self.lang["Mappings"]]
        self.defaults: dict = self.detamap.get(self.lang["Defaults"], dict())
        self.operations: dict = self.detamap.get(self.lang["Operations"], dict())
        self.source_info: dict = self.detamap[self.lang["Source"]]
        self.output_info: dict = self.detamap[self.lang["Output"]]

    def set_source(self, source) -> None:
        """Change the data source."""
        self.source = source

    def get_source(self):
        """Return the current source.
        
        :returns: self.source
        :rtype: str | path | dict | list"""
        return self.source
    
    def set_destination(self, destination) -> None:
        """Change destination or output."""
        self.destination = destination

    def get_destination(self):
        """Return the current destination.
        
        :returns: self.destination"""
        return self.destination

    def process(self) -> None:
        """
        Processes conversion for the currently loaded Detamap, data source, and destination.
        """
        data_generator = self._source_reader()

        # branch to determine output method called based on detamap.Output.argument for destination parameter
        # filepath as either string or Path object 
        if self.output_info["argument"] in self.lang.get("filepath", ["filepath"]):
            if self.output_info["type"] in self.lang.get("cast_string", ["str", "string"]):
                self.destination = Path(self.destination)

            # if not appending to existing file, delete if file exists and create new empty file
            if not self.output_info.get(self.lang.get("append", "append"), False) and self.destination.exists() and self.destination.is_file():
                self.destination.unlink()

            if self.destination.exists() and self.destination.is_file():
                new_file = False
            else:
                new_file = True
            self.destination.touch()

            with self.destination.open(mode="a",
                        buffering=self.output_info.get("buffering", -1),
                        encoding=self.output_info.get("encoding", "utf-8"),
                        errors=self.output_info.get("errors", None),
                        newline=self.output_info.get("newline", None)) as file:
                csv_writer = DictWriter(file,
                            fieldnames=self.output_info.get("fields"),
                            restval=self.output_info.get("restval", ""),
                            extrasaction=self.output_info.get("extrasaction", "raise"),
                            dialect=self.output_info.get("dialect", "excel"),
                            delimiter=self.output_info.get("delimiter", ","),
                            quotechar=self.output_info.get("quotechar", '"'),
                            escapechar=self.output_info.get("escapechar", None),
                            doublequote=self.output_info.get("doublequote", True),
                            skipinitialspace=self.output_info.get("skipinitialspace", False),
                            lineterminator=self.output_info.get("lineterminator", "\r\n"),
                            quoting=self.output_info.get("quoting", 0),
                            strict=self.output_info.get("strict", False))
                
                if new_file and not self.output_info.get(self.lang.get("omit_heading", "omit_heading"), False):
                    csv_writer.writeheader()
                for entry in data_generator:
                    row_data = {}
                    for source_field, destination_field in self.mappings.items():
                        row_data[destination_field] = entry[source_field]
                    csv_writer.writerow(row_data)
        elif self.output_info[self.lang.get("argument", "argument")] == "return":
            pass

    def _source_reader(self) -> Generator | dict | list:
        """
        Validate source type, and return a generator object if possible, otherwise return full object in accepted format.

        Source type should be defined in detamap under Source map.  Argument key defines what the source argument passed to Detakon() is (such as a filepath), and type key defines what sub-type to apply to that (such as filepath provided is a str or path object).

        Intent to add remote file, or result of API calls - giving consideration to add ability, or require calling application to submit data directly.
        
        :param self: Object reference.
        :returns: Generator object of dictionaries, or list/dictionary of dictionaries if generator not possible.
        :rtype: Generator | dict
        """
        # branch based on source.argument value provided in detamap

        # handler for source.argument being a filepath
        # filepath must be either a string to a file, or a Path object for a file.
        if self.source_info[self.lang.get("argument", "argument")] in self.lang.get("filepath", ["filepath"]):
            if self.source_info[self.lang.get("type", "type")] in self.lang.get("cast_string", ["str", "string"]):
                self.source = Path(self.source)
            if self.source.exists() and self.source.is_file():
                with self.source.open(mode='r',
                                        buffering=self.source_info.get("buffering", -1),
                                        encoding=self.source_info.get("encoding", "utf-8"),
                                        errors=self.source_info.get("errors", None),
                                        newline=self.source_info.get("newline", None)) as source_file:
                    # handler for source.format csv values.  if no source.format value is provided, csv value is default
                    if self.source_info.get("format", "csv") == "csv":
                        # DictReader defaults are used if Source does not contain a key for a given keyword.
                        # key:value paris can be provided in the detamap Source section to set the value of any DictReader keyword.
                        # values must conform with DictReader's expectation.
                        csv_reader = DictReader(source_file,
                                                fieldnames=self.source_info.get("fieldnames", None),
                                                restkey=self.source_info.get("restkey", None),
                                                restval=self.source_info.get("restval", None),
                                                dialect=self.source_info.get("dialect", "excel"),
                                                delimiter=self.source_info.get("separator", ","),
                                                quotechar=self.source_info.get("quotechar", '"'),
                                                escapechar=self.source_info.get("escapechar", None),
                                                doublequote=self.source_info.get("doublequote", True),
                                                skipinitialspace=self.source_info.get("skipinitialspace", False),
                                                lineterminator=self.source_info.get("lineterminator", "\r\n"),
                                                quoting=self.source_info.get("quoting", 0),
                                                strict=self.source_info.get("strict", False))
                        for row in csv_reader:
                            # insert default values if key missing or value is empty string
                            row = self._process_defaults(row)
                            # process operations
                            row = self._process_operations(row)
                            if row is not None:
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

    def _process_defaults(self, row):
        """Add default values to any missing column or empty string."""
        for key, value in self.defaults.items():
            if key not in row:
                row[key] = value
            elif row[key] == "" or row[key] == None:
                row[key] = value
        return row
    
    def _process_operations(self, row):
        """Process all operations from self.operations in order that operations appear in list."""
        for entry in self.operations:
            for operator, info in entry.items():
                operation = operator
                fields = info.get(self.lang.get("fields", "fields"))
                if fields == "*":
                    fields = row.keys()
                elif isinstance(fields, str):
                    fields = [fields]
                arguments = info.get(self.lang.get("arguments"), [])
                keyword_arguments = info.get(self.lang.get("keyword_arguments"), dict())

            for field in fields:
                # process string operations
                if operation in dir(str):
                    row[field] = getattr(row[field], operation)(*arguments, **keyword_arguments)
                elif operation.lower() in self.lang.get("slice", ["slice"]):
                    slice_object = slice(*(x if isinstance(x, int) else None for x in arguments))
                    row[field] = row[field][slice_object]
                elif operation.lower() in self.lang.get("hashmap", ["hashmap", "dictionary", "dict"]):
                    # print(f"before {operation}: {row[field]}")
                    hashmap = arguments[0]
                    if row[field] in hashmap.keys():
                        row[field] = hashmap[row[field]]
                    # print(f"after: {row[field]}")
                elif operation.lower() in self.lang.get("exclude", ["exclude"]):
                    if self._filter(row[field], *arguments):
                        return None
                elif operation.lower() in self.lang.get("include", ["include"]):
                    if not self._filter(row[field], *arguments):
                        return None
                elif operation.lower() in self.lang.get("cast", ["cast", "converttype", "convert type", "type cast", "typecast"]):
                    row[field] = self._cast_type(row[field], arguments)
                # creates a field if it does not exist. By default an empty string, otherwise equal to arguments.
                elif operation.lower() in self.lang.get("create field", ["create", "new", "create field", "new field"]):
                    if field not in row:
                        if len(arguments) > 0:
                            row[field] = arguments
                        else:
                            row[field] = ""
                elif operation.lower() in self.lang.get("duplicate", ["duplicate"]):
                    for argument in arguments:
                        if argument not in row:
                            row[argument] = row[field]
                        else:
                            raise ValueError(f"Operation '{operation}' failed: new field <{argument}> already exists.")
                # below operations are place holders, and may change operation names during implementation
                elif operation.lower() in ["mergefields", "merge", "union"]:
                    pass
                elif operation.lower() in ["splitfields", "split", "separate"]:
                    pass
                elif operation == "formatTime":
                    pass


        # print("---------Start Data Output ------------")
        # for key, value in row.items():
        #     print(f"{key}: {value} - Type: {type(value)}")
        # print("---------End Data Output ------------")
        return row

    def _load_detamap(self, detamap) -> dict:
        """
        Process object passed as detamap and return dictionary detamap.
        
        :param self: Object reference.
        :param detamap: Either a dictionary, JSON stream/string, or file path (string or pathlib.Path) to JSON file.
        :returns: dict of detamap
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

    def _filter(self, row_value, comparison: str, comparison_value) -> bool:
        """Take a string indicating a comparison to make, and a value that comparison will be made to, and return a bool indicating if that comparison is met.
        Designed for use in exclude and include filter operations.
        
        Filter comparison values and accepted aliases:

        * equal: "equal", "=", "==", "isequal", "is equal"
        * not equal: "not equal", "notequal", "!=", "~=", "<>", "not equals to", "not ="
        * in: "in", "contains", "substring"
        * not in: "not in", "notin"
        * greater than: "gt", "greaterthan", "greater than", ">"
        * less than: "lt", "lessthan", "less than", "<"
        * greater than or equal: "ge", "greater or equal", "greater than or equal", ">=", "≥"
        * less than or equal: "le", "less or equal", "less than or equal", "<=", "≤"
        * boolean: "bool", "boolean", "truthiness", "truthy", "falsy"
        * none: "isnone", "none"

        :param row_value: The value from the data source row to compare against comparison_value.
        :param comparison: The filter comparison operator to be used for the comparison.
        :param comparison_value: The value to compare the source value against.
        :returns: bool"""
        if comparison.lower() in self.lang.get("filter_equal", ["equal", "=", "==", "isequal", "is equal"]):
            return row_value == comparison_value
        elif comparison.lower() in self.lang.get("filter_not_equal", ["not equal", "notequal", "!=", "~=", "<>", "not equals to", "not ="]):
            return row_value != comparison_value
        elif comparison.lower() in self.lang.get("filter_in", ["in", "contains", "substring"]):
            return comparison_value in row_value
        elif comparison.lower() in self.lang.get("filter_not_in", ["not in", "notin"]):
            return comparison_value not in row_value
        elif comparison.lower() in self.lang.get("filter_greater_than", ["gt", "greaterthan", "greater than", ">"]):
            return row_value > comparison_value
        elif comparison.lower() in self.lang.get("filter_less_than", ["lt", "lessthan", "less than", "<"]):
            return row_value < comparison_value
        elif comparison.lower() in self.lang.get("filter_greater_or_equal", ["ge", "greater or equal", "greater than or equal", ">=", "≥"]):
            return row_value >= comparison_value
        elif comparison.lower() in self.lang.get("filter_less_or_equal", ["le", "less or equal", "less than or equal", "<=", "≤"]):
            return row_value <= comparison_value
        elif comparison.lower() in self.lang.get("filter_boolean", ["bool", "boolean", "truthiness", "truthy", "falsy"]):
            return bool(row_value)
        elif comparison.lower() in self.lang.get("filter_none", ["isnone", "none"]):
            return row_value is None
        else:
            raise ValueError(f"Could not find match for comparison operator: {comparison}")

    def _cast_type(self, value, data_type: str):
        """Cast value into the given type.  If type does not match an expected value raise a ValueError.
        
        Types values for casting, and accepted aliases:

        * int: "int", "integer", "long"
        * float: "float", "double"
        * Decimal: "decimal" (specifically the python type decimal.Decimal)
        * bool: "bool", "boolean"
        * str: "str", "string"
        
        :param value: value from source to cast into new type
        :param data_type: type to cast value to
        :returns: value as new type"""
        if data_type.lower() in self.lang.get("cast_int", ["int", "integer", "long"]):
            return int(value)
        elif data_type.lower() in self.lang.get("cast_float", ["float", "double"]):
            return float(value)
        elif data_type.lower() in self.lang.get("cast_decimal", ["decimal"]):
            return Decimal(value)
        elif data_type.lower() in self.lang.get("cast_boolean", ["bool", "boolean"]):
            return bool(value)
        elif data_type.lower() in self.lang.get("cast_string", ["str", "string"]):
            return str(value)
        else:
            raise ValueError(f"Unrecognized type value for cast: {data_type}")

    def _load_language(self, lang: str = "en-us") -> dict:
        """Returns translation dictionary for specified language.

        Language should be specified as ISO 639 language codes and ISO 3166 country codes seperated by a dash (-).  Default is en-us.

        ISO 639 set 1, 2, and 3 codes can be used.  `List of ISO 639 language codes <https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes>`_

        ISO 3166 A-2, A-3, and Num. codes can be used. `List of ISO 3166 country codes <https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes>`_

        :param lang: language code for specified language.  Defaults to en-us.
        :returns: translation dictionary."""
        if lang.lower() in ["english", "en", "eng", "en-us", "en-usa", "en-840", "eng-us", "eng-usa", "eng-840"]:
            from .languages import en_us
            return en_us.translation