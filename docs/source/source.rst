.. docs/source.rst

**************
Source Section
**************

The ``Source`` section is a dictionary of configuration settings to read the data source.

The :ref:`detamap-source-argument` setting is required.  :ref:`detamap-source-argument` describes the type of value the ``source`` argument passed to :class:`detakon.detakon.Converter` is.

Based on the context of the :ref:`detamap-source-argument` supplied, a ``type`` setting may also be required to further describe the type of the source argument supplied.

Fox example, the :ref:`detamap-source-argument-filepath` value for an :ref:`detamap-source-argument` can accept a value of ``"str"`` if a string representation of a path is supplied, or a ``"path"`` if source is a :py:class:`pathlib.Path`.

A :ref:`detamap-source-format` setting is also required to specify the structure or data type of the data contained in ``source``.

Source Settings
===============

Settings to control reading of the data source.  :ref:`detamap-source-argument` and :ref:`detamap-source-format` settings are required.

.. _detamap-source-argument:

argument
--------

The ``arguments`` setting describes what type of argument was passed to the :class:`detakon.detakon.Converter` as a ``source`` parameter.

This setting is required.

.. _detamap-source-argument-filepath:

``filepath``
^^^^^^^^^^^^
    Supplying the ``"filepath"`` value to the argument setting describes the source as being a file path.  It expects the source argument provided to :class:`detakon.detakon.Converter` to be a :py:class:`pathlib.Path`.

    A additional ``"type"`` setting can be provided in the ``Source`` section to modify the python type provided as an argument, when the ``argument`` can accept other types of values.

    Other accepted ``"type"`` values for ``"filepath"``:

    * ``"str"`` - to be used if the filepath supplied is a string.


.. _detamap-source-format:

format
------

The ``format`` setting should specify the stucture or data type contained in the ``source`` to :class:`detakon.detakon.Converter`.

This setting is required.

.. _detamap-source-format-csv:

``csv``
^^^^^^^
    To be used for data structured as Comma Separated Values (CSV), or similar data that can be read by Python's :py:class:`csv.DictReader` class in the :py:mod:`csv` module.

    Detakon uses :py:class:`csv.DictReader` to read CSV source data.  Any additional settings can be provided that matches the parameters that :py:class:`csv.DictReader` accepts.

    For example, a ``delimiter`` setting can be supplied to change the delimiter used in the data, such as to read Tab Separated Value (TSV) data, or an ``encoding`` setting can be supplied to change the character encoding.

    See the Python Docs for `DictReader <https://docs.python.org/3/library/csv.html#csv.DictReader>`_ for more details.

Examples
========

.. code-block:: json-object

    "Source": {
        "argument": "filepath",
        "type": "str",
        "encoding": "utf-8",
        "format": "csv",
        "delimiter": ","
    }