.. docs/detamap.rst

**************
Detamaps
**************

Detamaps are JSON or TOML configuration files that the ``detakon`` library uses to process data converstion.

.. tip::
    Sections or keys below in *italics* are optional.

##############
Major Sections
##############

Detamaps have five primary sections with the following keys:

* Mappings - A dictionary of source fields mapped to the output field names.
* *Defaults* - A dictionary containing default values to be used for given source fields.
* *Operations* - A list of operations/transformations to be performed in order.
* Source - A dictionary of configuration arguments to read the data source.
* Output - A dictionary of configuration arguments used for outputting data.

########################
Settings & Configuration
########################

Detamaps have the following keys for settings and configuration:

* *lang* - A string indicating the language the Detamap is written in (default: "en-us").

#######################
Detailed Specifications
#######################

.. toctree::
   :maxdepth: 1

   mappings
   defaults
   operations
   source
   output
   lang