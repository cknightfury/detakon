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
        "hashmap": ["hashmap", "dictionary", "dict"],
        "slice": ["slice"],
        "exclude": ["exclude"],
        "include": ["include"],
        "cast": ["cast", "converttype", "convert type", "type cast", "typecast"],
        "create field": ["create", "new", "create field", "new field"],
        "duplicate": ["duplicate"],
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