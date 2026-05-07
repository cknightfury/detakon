# Contains operations available to and used by Detakon
# Operations accept a dictionary (row of data), args, kwargs.
# Operations should return a dictionary (row of data), or None (if row should be discarded/filtered out).

from detakon.translation_framework import load_language

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

def filter(row_value: dict, comparison: str, comparison_value, *args, language_map: dict = load_language("en-us")) -> bool:
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

def _cast_type(value, data_type: str):
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