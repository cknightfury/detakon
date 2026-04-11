.. docs/operations.rst

******************
Operations Section
******************

The ``Operations`` section is a list of operations/transformations to be performed in order.

Each operation should be added as a dictionary to the ``Operations`` list in the order to be performed.

The name of the operation to be performed should be provided as the key, which will contain a nested dictionary of key-value pairs for ``fields``, ``args``, and ``kwargs``.

What needs to be provided as a value to each key is contextual to the operation being performed, but generally:

* ``fields`` are a list of fields the operation will be applied to.

    * If the string '*' is supplied instead of a list, the operation is applied to all currently existing fields.
    * If any other string is provided, the string is converted to a list with only that string as an entry.

* ``args`` are the arguments to be supplied to the operation.
* ``kwargs`` are keyword-arguments the operation may use.

The ``Operations`` section is optional.

Available Operations
====================

Python String Methods
---------------------

Any Python :py:mod:`string` method should be accessible as an operation.

The values supplied to the ``args`` list should be the same order of arguments supplied to the appropriate method.

Appropriate keyword arguments can be supplied using a nested dictionary with the key ``kwargs``.

If the method does not require any ``args`` or ``kwargs``, then these items can be omitted.

String Method Examples
^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: json-object

    "Operations": [
        {"split": {"fields": "Phone 1", "kwargs": {"sep": "-"}}},
        {"upper": {"fields": ["Email", "Last Name", "First Name"]}}
    ]

slice
-----

To enable Python like slices (such as ``"String to slice"[0, -3]``), Detakon implements the slice operation using the Python :py:func:`slice` function to generate a slice_object.

The first value supplied in the ``args`` list should be the start for the slice, and the second should be the stop of the slice.

Values should be integers. If a non-integer value is provided, it is assumed to be None.

Indexing begins at 0, and negative values can be used.

Slice Examples
--------------

.. code-block:: json-object

    "Operations": [
        {"slice": {"fields": ["Phone Number"],
                    "args": [0, -3]}}
    ],

hashmap
=======

The hashmap operation takes a single dictionary argument to the ``args`` list, and replaces each key found in the source with the matching value.

Hashmap Examples
----------------

.. code-block:: json-object

    "Operations": [
        {"hashmap": {"fields": "Country",
                        "args": [{
                            "United States of America": "USA",
                            "United States": "USA",
                            "US": "USA",
                            "Canada": "CAN",
                            "Antarctica (the territory South of 60 deg S)": "Antarctica"}]
                        }
                    }
    ]

Filter Operations
=================

There are two operations to filter data.

To use a filter on fields, supply two values to the ``args`` list.  The first value should be a conditional to test, and the second value should be the value to test the field against.

exclude
    Remove rows where the value of a given field meets a conidtional.

include
    Keeps only rows where the value of a given field meets a conditional.

Filter Conditionals
-------------------

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

Filter Examples
---------------

.. code-block:: json-object

    "Operations": [
        {"include": {"fields": "Last Name",
                    "args": ["equal", "SMITH"]}}
    ]

.. code-block:: json-object

    "Operations": [
        {"exclude": {"fields": "Total",
                    "args": ["<", 100.00]}}
    ]

Examples
========

.. code-block:: json-object

    "Operations": [
        {"hashmap": {"fields": "Country",
                        "args": [{
                            "United States of America": "USA",
                            "United States": "USA",
                            "US": "USA",
                            "Canada": "CAN",
                            "Antarctica (the territory South of 60 deg S)": "Antarctica"}]
                        }
                    },
        {"duplicate": {"fields": "Phone 1", "args": ["temp_phone"]}},
        {"split": {"fields": "Phone 1", "kwargs": {"sep": "-"}}},
        {"upper": {"fields": ["Email", "Last Name", "First Name"]}}
    ]