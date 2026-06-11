# Contains operations available to and used by Detakon
# Operations accept a dictionary (row of data), args, kwargs.
# Operations should return a dictionary (row of data), or None (if row should be discarded/filtered out).

# Operations are typically performed in-place unless otherwise specified.  change_place can be used to use the field as a source, but output result of the operation to another field.

from detakon.translation_framework import load_language
from decimal import Decimal

def make_list(field: str, row: dict, *args, **kwargs) -> dict:
    """Make a list from all fields in args.  Specified field will be the destination, and any existing data will be overwritten.
    
    :param field: Field destination for list.
    :param row: A dictionary of data that holds the fields to be operated on.
    :param *args: Fields to append to list to be stored in destination field.
    :param **kwargs: Keyword arguments to be passed."""
    row[field] = [row[arg] for arg in args]
    return row

def string_join(field: str, row: dict, *args, **kwargs) -> dict:
    """Calls str.join on list in specified field and uses args[0] as the separator for the resulting string.  Return the updated row.
    
    :param field: Field used as data source.  Must contain a list that str.join can operate on.
    :param row: A dictionary of data that holds the field to be operated on.
    :param *args: List of which args[0] is expected to be a string to be used as a separator.
    :param **kwargs: Keyword arguments to be passed."""
    separator = args[0]
    row[field] = separator.join(row[field])
    return row

def change_place(field: str, row: dict, destination: str, operation: str, args, kwargs, language_map: dict) -> dict:
    """Changes an in-place operation into an out-of-place operation.
    
    Calls the specified operation on a copy of the row, and merge the specified row from the copy back into the original with a different key.
    
    :param field: Field used as data source.
    :param row: A dictionary of data that holds the field to be operated on.
    :param destination: The name of the field to store the result of the operation.
    :param *args: Arguments to be passed to the operation.
    :param **kwargs: Keyword arguments to be passed to the operation."""
    if operation in language_map.get("slice"):
        copy_row = slice_field(field, row.copy(), *args, **kwargs)
    elif operation in language_map.get("hashmap"):
        copy_row = hashmap(field, row.copy(), *args, **kwargs)
    else:
        return row
    row[destination] = copy_row[field]
    return row


def slice_field(field: str, row: dict, *args, **kwargs) -> dict:
    """Perform a slice on a field from a row of data and return the row with the updated sliced field.
    
    :param field: The key for the value being sliced.
    :param row: A dictionary of data that holds the field to be sliced.
    :param *args: Arguments to be passed to python's slice object.
    :param **kwargs: Keyword arguments to be passed to python's slice object."""
    slice_object = slice(*args, **kwargs)
    row[field] = row[field][slice_object]
    return row

def hashmap(field: str, row: dict, *args, **kwargs) -> dict:
    """Convert value of field in row to new value from dictionary args[0] if value of field matches key in dict args[0] and return updated row.
    
    :param field: The key for the value being value being converted.
    :param row: A dictionary of data that holds the field to be converted.
    :param *args: List of which args[0] is expected to be a dictionary of mappings from old value to new value.  Keys are case sensitive.
    :param **kwargs: Keyword arguments to be passed."""
    hashmap = args[0]
    if row[field] in hashmap.keys():
        row[field] = hashmap[row[field]]
    return row

def create_field(field: str, row: dict, *args, **kwargs) -> dict:
    """Add field to source dictionary. By default new fields are empty strings.

    If args are supplied:
    * List of length one: Assign first value to field.
    * List of length greater than one: Assign list of args to field.
    
    :param field: The name of the field to be created.
    :param row: A dictionary of data that holds the current state of the row.
    :param *args: If supplied, args[0] will be used to set the value of the field.
    :param **kwargs: Keyword arguments to be passed."""

    if field not in row:
        if len(args) > 1:
            row[field] = args
        elif len(args) > 0:
            row[field] = args[0]
        else:
            row[field] = ""
    return row

def duplicate(field: str, row: dict, *args, **kwargs) -> dict:
    """Creates new fields with the value contained in field.  Each value in args will be the name of the new fields created by duplicating field.
    
    :param field: The name of the field to be duplicated.
    :param row: A dictionary of data that holds the current state of the row.
    :param *args: A list of fields be created with the duplicated value.
    :param **kwargs: Keyword arguments to be passed."""

    for argument in args:
        if argument not in row:
            row[argument] = row[field]
        else:
            raise ValueError(f"Operation <duplicate> failed: new field <{argument}> already exists.")
    return row

def duplicate_row(field: str, row: dict, *args, **kwargs) -> dict:
    """Causes row to be appended to output multiple times based on value of field. Value must be int or castable into int.
    
    Adds a special key to row called ``detakon_duplicate_rows`` that contains an int quantity.

    :param field: Field with the value specifying quantity of times to output row.
    :param row: A dictionary of data that holds the current state of the row.
    :param *args: Additional arguments being passed.
    :param **kwargs: Keyword arguments to be passed."""

    row["detakon_duplicate_rows"] = int(row[field])
    return row

def filter(row_value: dict, comparison: str, comparison_value, *args, language_map: dict = load_language("en-us"), **kwargs) -> bool:
    """Take a string indicating a comparison to make, and a value that comparison will be made to, and return a bool indicating if that comparison is met.
    Designed for use in exclude and include filter operations.
    
    For clarity, please see shorter version of function header below:

    ``detakon.operations.filter(row_value: dict, comparison: str, comparison_value, *args, language_map: dict = load_language("en-us"), **kwargs) → bool``

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
    :param language_map: The language map to use for comparation aliases.  Defaults to "en-us".
    :returns: bool"""
    if comparison.lower() in language_map.get("filter_equal", ["equal", "=", "==", "isequal", "is equal"]):
        return row_value == comparison_value
    elif comparison.lower() in language_map.get("filter_not_equal", ["not equal", "notequal", "!=", "~=", "<>", "not equals to", "not ="]):
        return row_value != comparison_value
    elif comparison.lower() in language_map.get("filter_in", ["in", "contains", "substring"]):
        return comparison_value in row_value
    elif comparison.lower() in language_map.get("filter_not_in", ["not in", "notin"]):
        return comparison_value not in row_value
    elif comparison.lower() in language_map.get("filter_greater_than", ["gt", "greaterthan", "greater than", ">"]):
        return row_value > comparison_value
    elif comparison.lower() in language_map.get("filter_less_than", ["lt", "lessthan", "less than", "<"]):
        return row_value < comparison_value
    elif comparison.lower() in language_map.get("filter_greater_or_equal", ["ge", "greater or equal", "greater than or equal", ">=", "≥"]):
        return row_value >= comparison_value
    elif comparison.lower() in language_map.get("filter_less_or_equal", ["le", "less or equal", "less than or equal", "<=", "≤"]):
        return row_value <= comparison_value
    elif comparison.lower() in language_map.get("filter_boolean", ["bool", "boolean", "truthiness", "truthy", "falsy"]):
        return bool(row_value)
    elif comparison.lower() in language_map.get("filter_none", ["isnone", "none"]):
        return row_value is None
    else:
        raise ValueError(f"Could not find match for comparison operator: {comparison}")

def cast_type(value, data_type: str, *args, language_map: dict = load_language("en-us"), **kwargs):
    """Cast value into the given type.  If type does not match an expected value raise a ValueError.
    
    For clarity, please see shorter version of function header below:
    
    ``detakon.operations.cast_type(value, data_type: str, *args, language_map: dict = load_language("en-us"), **kwargs)``

    Types values for casting, and accepted aliases:

    * int: "int", "integer", "long"
    * float: "float", "double"
    * Decimal: "decimal" (specifically the python type decimal.Decimal)
    * bool: "bool", "boolean"
    * str: "str", "string"
    
    :param value: value from source to cast into new type
    :param data_type: type to cast value to
    :param language_map: The language map to use for comparation aliases.  Defaults to "en-us".
    :returns: value as new type"""
    if data_type.lower() in language_map.get("cast_int", ["int", "integer", "long"]):
        return int(value)
    elif data_type.lower() in language_map.get("cast_float", ["float", "double"]):
        return float(value)
    elif data_type.lower() in language_map.get("cast_decimal", ["decimal"]):
        return Decimal(value)
    elif data_type.lower() in language_map.get("cast_boolean", ["bool", "boolean"]):
        return bool(value)
    elif data_type.lower() in language_map.get("cast_string", ["str", "string"]):
        return str(value)
    else:
        raise ValueError(f"Unrecognized type value for cast: {data_type}")

###################
# Math Operations #
###################

# Math operations use the fields values as destinations of the operations.
# Math operations are typically intended to have one value passed to fields.
# The operation is performed subsequently on each field passed to args, with the final output being assigned to the destination specified in fields.
# If a field in args contains a list, the operation is sequentially performed on each element of the list, before continuing to the next field.

def flatten_lists(element):
    unflattened_list = list(element)
    flatened_list = []
    while unflattened_list:
        element = unflattened_list.pop(0)
        if isinstance(element, (list, tuple)):
            unflattened_list = list(element) + unflattened_list
        else:
            flatened_list.append(element)
    return flatened_list

def sum_operation(field: str, row: dict, *args, **kwargs) -> dict:
    """Sum each field in args, and return the total to the specified field.

    By default, summation starts at 0.  To set a start value either:

    * Pass a field name for the start value to kwargs with the key "start_field"
    * Pass a number as the start value to kwargs with the key "start_value"
    
    :param field: Field used as destination of calculation.
    :param row: A dictionary of data that holds the fields to be operated on.
    :param *args: List of fields the operation is to be performed on.
    :param **kwargs: Keyword arguments to be passed."""

    if "start_field" in kwargs:
        total = kwargs["start_field"]
    elif "start_value" in kwargs:
        total = kwargs["start_value"]
    else:
        total = 0

    for arg in args:
        value = row[arg]
        if isinstance(value, (list, tuple)):
            total += sum(flatten_lists(value))
        else:
            items = []
            items.append(value)
            total += sum(items)

    row[field] = total
    return row

def subtract_operation(field: str, row: dict, *args, **kwargs) -> dict:
    """Subtract each field in args, and return the total to the specified field.
    
    By default, subtraction starts at 0.  To set a start value either:

    * Pass a field name for the start value to kwargs with the key "start_field"
    * Pass a number as the start value to kwargs with the key "start_value"

    :param field: Field used as destination of calculation.
    :param row: A dictionary of data that holds the fields to be operated on.
    :param *args: List of fields the operation is to be performed on.
    :param **kwargs: Keyword arguments to be passed."""

    if "start_field" in kwargs:
        total = kwargs["start_field"]
    elif "start_value" in kwargs:
        total = kwargs["start_value"]
    else:
        total = 0

    for arg in args:
        value = row[arg]
        if isinstance(value, (list, tuple)):
            total -= sum(flatten_lists(value))
        else:
            items = []
            items.append(value)
            total -= sum(items)

    row[field] = total
    return row