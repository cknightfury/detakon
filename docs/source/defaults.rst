.. docs/defaults.rst

****************
Defaults Section
****************

The ``Defaults`` section is a dictionary containing default values to be used for given source fields.

If a field is blank/empty, the value for the corresponding key will be inserted.

If a field does not exist in the source data, the field is created using the corresponding ``Defaults`` value.

########
Examples
########

.. code-block:: json-object

    "Defaults": {
        "Country": "Canada",
        "Province": "ON",
        "Carrier": "Canada Post",
        "Total": 0.00
    }