.. docs/mappings.rst

****************
Mappings Section
****************

The ``Mappings`` section is a dictionary of source fields mapped to the output field names.

Keys should be the source fields.  Keys do not need to exist in the source file if a ``Defaults`` or ``Operation`` creates the field during processing.

``Mappings`` should only contain fields that will be in the final output.

The order of fields in ``Mappings`` does not determine the order of fields in the output.  The order of fields in the output is determined by supplying a list of fields to the ``field`` key in the :doc:`Output Section <output>`.

########
Examples
########

.. code-block:: json-object

    "Mappings": {
        "Customer Id": "External ID",
        "First Name": "First Name",
        "Last Name": "Last Name",
        "Country": "Country",
        "Phone 1": "Phone",
        "Phone 2": "Cell",
        "Email": "Email",
        "Postal Code": "Zip"
    }