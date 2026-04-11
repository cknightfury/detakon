.. docs/output.rst

**************
Output Section
**************

The ``Output`` section is a dictionary of configuration settings for outputting data to the destination.

The :ref:`detamap-output-argument` setting is required.  :ref:`detamap-output-argument` describes the type of value the ``destination`` argument passed to :class:`detakon.detakon.Converter` is.

Based on the context of the :ref:`detamap-output-argument` supplied, a ``type`` setting may also be required to further describe the type of the output argument supplied.

Fox example, the :ref:`detamap-output-argument-filepath` value for an :ref:`detamap-output-argument` can accept a value of ``"str"`` if a string representation of a path is supplied, or a ``"path"`` if output is a :py:class:`pathlib.Path`.

A :ref:`detamap-output-format` setting is also required to specify the structure or data type of the data being output.

Output Settings
===============

Settings to control data being output.  :ref:`detamap-output-argument`, :ref:`detamap-output-fields`, and :ref:`detamap-output-format` settings are required.

.. _detamap-output-argument:

argument
--------

The ``arguments`` setting describes what type of argument was passed to the :class:`detakon.detakon.Converter` as a ``destination`` parameter.

This setting is required.

.. _detamap-output-argument-filepath:

``filepath``
^^^^^^^^^^^^
    Supplying the ``"filepath"`` value to the argument setting describes the destination as being a file path.  It expects the destination argument provided to :class:`detakon.detakon.Converter` to be a :py:class:`pathlib.Path`.

    A additional ``"type"`` setting can be provided in the ``Output`` section to modify the python type provided as an argument, when the ``argument`` can accept other types of values.

    Other accepted ``"type"`` values for ``"filepath"``:

    * ``"str"`` - to be used if the filepath supplied is a string.

.. _detamap-output-fields:

fields
------

The ``fields`` setting should be a list of field names as strings, in the order fields should be in the outputted data.  Some output formats may not have an order, but this setting is still required, as it may be used internally for other purposes.

This setting is required.

.. _detamap-output-format:

format
------

The ``format`` setting should specify the stucture or data type that will be outputted to the destination supplied to :class:`detakon.detakon.Converter`.

This setting is required.

.. _detamap-output-format-csv:

``csv``
^^^^^^^
    To be used for data structured as Comma Separated Values (CSV), or similar data that can be written by Python's :py:class:`csv.DictWriter` class in the :py:mod:`csv` module.

    Detakon uses :py:class:`csv.DictWriter` to format CSV output.  Any additional settings can be provided that matches the parameters that :py:class:`csv.DictWriter` accepts.

    For example, a ``delimiter`` setting can be supplied to change the delimiter used in the data, such as to read Tab Separated Value (TSV) data, or an ``encoding`` setting can be supplied to change the character encoding.

    See the Python Docs for `DictWriter <https://docs.python.org/3/library/csv.html#csv.DictWriter>`_ for more details.


Examples
========

.. code-block:: json-object

    "Output": {
        "fields": ["External ID", "Company", "Last Name", "First Name", "Country", "Zip", "Phone", "Cell", "Email", "URL"],
        "argument": "filepath",
        "type": "str",
        "append": false,
        "omit_heading": false,
        "encoding": "utf-8",
        "format": "csv",
        "delimiter": ","
    }