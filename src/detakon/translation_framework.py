def load_language(self, lang: str = "en-us") -> dict:
    """Returns translation dictionary for specified language.

    Language should be specified as ISO 639 language codes and ISO 3166 country codes seperated by a dash (-).  Default is en-us.

    ISO 639 set 1, 2, and 3 codes can be used.  `List of ISO 639 language codes <https://en.wikipedia.org/wiki/List_of_ISO_639_language_codes>`_

    ISO 3166 A-2, A-3, and Num. codes can be used. `List of ISO 3166 country codes <https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes>`_

    :param lang: language code for specified language.  Defaults to en-us.
    :returns: translation dictionary."""
    if lang.lower() in ["english", "en", "eng", "en-us", "en-usa", "en-840", "eng-us", "eng-usa", "eng-840"]:
        from .languages import en_us
        return en_us.translation