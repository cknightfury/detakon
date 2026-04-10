.. docs/detamap.rst

**************
Detamaps
**************

Detamaps are JSON or TOML configuration files that the ``detakon`` library uses to process data converstion.

.. warning::
    TOML Detamap compatibility is still in development, and not available at this time. 

######################
Vocabulary at a Glance
######################

This documentation is making a concious decision to use Python terminology when referring to Detamap structure, instead of JSON, or TOML terminology.

.. list-table:: Detamap Vocabulary Comparison
    :header-rows: 1

    * - Detamap Term
      - Description
      - JSON Term
      - TOML Term
    * - Dictionary
      - Key-value pairs contained in curly braces: {}
      - Object
      - Table
    * - Item
      - A single key-value pair in a dictionary.
      - Member
      - Key/Value Pair
    * - Key
      - The value on the left side of a key-value pair.
      - Name
      - Key
    * - Value
      - The value on the right side of a key-value pair.
      - Value
      - Value
    * - List
      - A sequence of values contained in brackets: []
      - Array
      - Array

Nested Dictionary
    A dictionary inside of another dictionary.

Section
    A root item that instead of a value, the key contains either a nested dictionary, or list of operations.

Operation
    A nested dictionary that contains the name of a function, method, or transformation to run as it's key, and items in the value that define how the function will operate.

Field
    Individual name of a value from the data source or destination.  Also can be thought of as a column name in tablular data.

Setting
    Any item connected to the root that is not a section.  Settings will be reffered to as the name of the key for the setting.  Such as the :doc:`lang`

.. tip::
    Sections or settings below in *italics* are optional.

##############
Major Sections
##############

Detamaps have five primary sections:

* Mappings - A dictionary of source fields mapped to the output field names.
* *Defaults* - A dictionary containing default values to be used for given source fields.
* *Operations* - A list of operations/transformations to be performed in order.
* Source - A dictionary of configuration arguments to read the data source.
* Output - A dictionary of configuration arguments used for outputting data.

########################
Settings & Configuration
########################

Detamaps have the following items for settings and configuration:

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