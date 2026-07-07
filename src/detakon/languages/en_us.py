translation = {
    # Primary keys
    "Mappings": "Mappings",
    "Defaults": "Defaults",
    "Operations": "Operations",
    "Source": "Source",
    "Output": "Output",
    # Operations
        "fields": "fields",
        "arguments": "args",
        "keyword_arguments": "kwargs",
        "list": ["list", "make_list"],
        "join": ["join"],
        "hashmap": ["hashmap", "dictionary", "dict"],
        "slice": ["slice"],
        "exclude": ["exclude"],
        "include": ["include"],
        "cast": ["cast", "converttype", "convert type", "type cast", "typecast"],
        "create field": ["create", "new", "create field", "new field"],
        "duplicate": ["duplicate"],
        "duplicate_rows": ["duplicate_rows", "duplicate rows", "duplicate-row", "duplicate_row", "duplicate row", "duplicate-rows", "union duplicates"],
        "outofplace": ["change place", "change_place", "changeplace", "change-place", "outofplace", "out of place", "out-of-place", "out_of_place", "not-in-place", "not in place", "not_in_place"],
        "sum": ["sum", "add", "+", "addition"],
        "subtract": ["subtract", "difference", "-", "subtraction"],
        # Include and exclude filters
        "filter_equal": ["equal", "=", "==", "isequal", "is equal"],
        "filter_not_equal": ["not equal", "notequal", "!=", "~=", "<>", "not equals to", "not ="],
        "filter_in": ["in", "contains", "substring"],
        "filter_not_in": ["not in", "notin"],
        "filter_greater_than": ["gt", "greaterthan", "greater than", ">"],
        "filter_less_than": ["lt", "lessthan", "less than", "<"],
        "filter_greater_or_equal": ["ge", "greater or equal", "greater than or equal", ">=", "≥"],
        "filter_less_or_equal": ["le", "less or equal", "less than or equal", "<=", "≤"],
        "filter_boolean": ["bool", "boolean", "truthiness", "truthy", "falsy"],
        "filter_none": ["isnone", "none"],
        "datetime": ["to_datetime", "to datetime","date", "datetime", "time", "string_to_datetime", "string to datetime", "to_date", "to date", "to_time", "to time", "todatetime", "todate", "totime"],
        "datestring": ["from_datetime", "from datetime", "datestring", "datetime_to_string", "datetime to string", "from_date", "from date", "from_time", "from time", "fromdatetime", "fromdate", "fromtime"],
        # Type casting
        "cast_int": ["int", "integer", "long"],
        "cast_float": ["float", "double"],
        "cast_decimal": ["decimal"],
        "cast_boolean": ["bool", "boolean"],
        "cast_string": ["str", "string"],
    # Source and Output
        "argument": "argument",
        "type": "type",
        # Options for DictReader not included in translation
        # They are part of python and should be provided as python expects
        "filepath": ["filepath"],
        # reusing cast_string instead of making separate "str" key
        "append": "append", # Append output to file if exists
        "omit_heading": "omit_heading" # Do not output headings
}