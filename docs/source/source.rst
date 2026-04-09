.. docs/source.rst

**************
Source Section
**************

The ``Source`` section is a dictionary of configuration arguments to read the data source.

The ``argument`` member is required.  ``argument`` describes the type of value the ``source`` argument passed to ``detakon.detakon.Converter`` is.

Based on the context of the ``argument`` supplied, a ``type`` key may also be required to further describe the type of the source argument supplied.

Fox example, the "filepath" value for an ``argument`` can accept a type of "str" if a string representation of a path is supplied, or a "path" if source is a :py:class:`pathlib.Path` type.

A ``format`` key is also required to specify the structure or data type of of the data contained in ``source``.

##############
Source Members
##############

arguments
=========

The ``arguments`` member describes what type of argument was passed to the :class:`detakon.detakon.Converter` as a ``source`` argument.

``filepath``
    The "filepath" argument describes the source as being a file path.  It expects the source argument provided to ``detakon.detakon.Converter`` to be a :py:class:`pathlib.Path`.

    A additional ``type`` member can be provided in the ``Source`` section to clarify the python type was provided as an argument, when the ``argument`` has multiple possible types.

    Other accepted ``type`` values:

    * "str" - to be used if the filepath supplied is a string.


format
======

The ``format`` member should specify the stucture or data type contained in the ``source`` to :class:`detakon.detakon.Converter`.

This key is required.

``csv``
    To be used for data structed as a Comma Separated Value, or similar data that can be read by Python's :py:class:`csv.DictReader` library.

    ``Detakon`` uses :py:class:`csv.DictReader` to read the file.  Any additional members can be provided that matches the parameters that :py:class:`csv.DictReader` accepts.

    For example, a ``delimiter`` key can be supplied to change the delimiter used in the data, such as to read Tab Separated Value data.  Or an ``encoding`` key can be supplied to change the character encoding.

    See the Python Docs for `DictReader <https://docs.python.org/3/library/csv.html#csv.DictReader>`_ for more details.

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