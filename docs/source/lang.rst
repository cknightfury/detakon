.. docs/lang.rst

**************************
Changing Detamap Languages
**************************

The ``lang`` Setting
====================

A Detamap may include a ``lang`` setting that can aid in accepting various languages and dialects.

The value provided to the ``lang`` setting should be the 2 character `ISO 639 <https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes>`_ code, followed by a dash (-) followed by a 2 or 3 character `ISO 3166 <https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes>`_ code.

``lang`` can also take a number of aliases, which are defined by the :meth:`detakon.detakon.Converter._load_language()` method and are mapped to the corresponding file in the ``src/detakon/languages`` directory.  Typically an alias will exist for each combination of `ISO 639 <https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes>`_ (2-character and 3-character) codes and `ISO 3166 <https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes>`_ (2-character, 3-character, and 3-digit) codes.

If ``lang`` is not present in the Detamap, ``en-us`` is loaded by default.

Available Languages
===================

Currently defined languages:

* ``en-us``

Examples
========

.. code-block:: json-object

    "lang": "en-us"
