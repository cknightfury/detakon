.. docs/operations.rst

******************
Operations Section
******************

The ``Operations`` section is a list of operations/transformations to be performed in order.

Each operation should be added as a dictionary to the ``Operations`` list in the order to be performed.

The name of the operation to be performed should be provided as the key, which will contain a sub-dictionary of key-value pairs for ``fields``, ``args``, and ``kwargs``.

What needs to be provided as a value to each key is contextual to the operation being performed, but generally:

* ``fields`` are a list of fields the operation will be applied to.

    * If the string '*' is supplied instead of a list, the operation is applied to all currently existing fields.
    * If any other string is provided, the string is converted to a list with only that string as an entry.

* ``args`` are the arguments to be supplied to the operation.
* ``kwargs`` are keyword-arguments the operation may use.

The ``Operations`` section is optional.

########
Examples
########

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