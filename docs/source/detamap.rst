.. docs/detamap.rst

**************
Detamaps
**************

Detamaps are JSON or TOML configuration files that the ``detakon`` library uses to process data converstion.

#################
Detamap Sections
#################

Detamaps have five primary sections with the following keys:

* Mappings - A dictionary of source fields mapped to the output field names.
* Defaults - A dictionary containing default values to be used for given source fields.
* Operations - A list of operations/transformations to be performed in order.
* Source - A dictionary of configuration arguments to read the data source.
* Output - A dictionary of configuration arguments used for outputting data.