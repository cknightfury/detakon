.. docs/source.rst

**************
Source Section
**************

The ``Source`` section is a dictionary of configuration arguments to read the data source.

The ``argument`` key is required.  ``argument`` describes what type of value the ``source`` argument passed to ``detakon.detakon.Converter`` is.

Based on the context of the ``argument`` supplied, a ``type`` key may also be required to further describe the type of the source argument supplied.

Fox example, the "filepath" value for an ``argument`` can accept a type of "str" if a string representation of a path is supplied, or a "path" if source is a ``pathlib.Path`` type.

########
Examples
########

.. code-block:: json-object

    "Source": {
        "argument": "filepath",
        "type": "str",
        "encoding": "utf-8",
        "format": "csv",
        "delimiter": ","
    }