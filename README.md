# detakon

[![PyPI - Version](https://img.shields.io/pypi/v/detakon.svg)](https://pypi.org/project/detakon)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/detakon.svg)](https://pypi.org/project/detakon)

-----

## Description

A data converter than uses configuration files (referred to as [detamaps](https://detakon.readthedocs.io/en/latest/detamap.html)) to map fields in the source data to output data, and perform operations on the data before outputting.  Detamaps may also contain configuration data for the data source and output, and defaults to use if fields are missing, or blank/empty.

> [!NOTE]
> Detakon is in early development and may have breaking changes between versions.  Detamaps, methods, and usage may change between minor versions until version 1.0 release.
> After version 1.0 release, any breaking changes will result in a major version bump.
> Recommended to use PyPI version. Version in source code is next planned release on PyPI, and is not official until pushed to PyPI.

## Table of Contents

- [Documentation](#documentation)
- [Installation](#installation)
- [Usage](#usage)
- [Detamap Files](#detamap-files)
- [License](#license)

## Documentation

The latest documentation can be found at [https://detakon.readthedocs.io/](https://detakon.readthedocs.io/)

For older versions of documentation, they can be found inside your copy of the respository under the "/docs" directory and built using Sphinx.  The first version that contained documentation was v0.3.0.

## Installation

```console
pip install detakon
```

## Usage

> [!WARNING]
> Status: Currently in pre-release, as minimal viable product for CSV to CSV conversions only.  Not for usage in production systems, breaking changes are coming in future releases.
> Some planned changes can be viewed in the [ROADMAP.md](https://github.com/cknightfury/detakon/blob/main/ROADMAP.md) file.

Converter(detamap, source, destination).process()

Sample:

```
from detakon.detakon import Converter

invoice_converter = Converter("invoice_detamap.json", "data_dump_2026-01-01.csv", "invoice_2026-01-01.csv")
invoice_converter.process()
```

## Detamap Files

A detamap configuration file is used to provide all details necessary for the data conversion.

A datamap must be a Python dictionary, or convertable to a Python dictionary.  Currently this means either a dictionary or JSON file (plans to add TOML support).

Please see the documentation for more detail on [detamaps](https://detakon.readthedocs.io/en/latest/detamap.html).

A detamap typically has the following sections:
- ["Mappings"](https://detakon.readthedocs.io/en/latest/mappings.html)
- ["Defaults"](https://detakon.readthedocs.io/en/latest/defaults.html)
- ["Operations"](https://detakon.readthedocs.io/en/latest/operations.html)
- ["Source"](https://detakon.readthedocs.io/en/latest/source.html)
- ["Output"](https://detakon.readthedocs.io/en/latest/output.html)

A detamap JSON file may look similar to:

```
{
    "Mappings": {
        "Customer Id": "External ID",
        "First Name": "First Name",
        "Last Name": "Last Name",
        "Company": "Company",
        "Country": "Country",
        "Phone 1": "Phone",
        "Phone 2": "Cell",
        "Email": "Email",
        "Website": "URL",
        "Postal Code": "Zip"
    },
    "Defaults": {
        "Postal Code": "00000"
    },
    "Operations": [
        {"hashmap": {"fields": "Country",
                        "arguments": [{
                            "United States of America": "USA",
                            "Antarctica (the territory South of 60 deg S)": "Antarctica"}]
                        }
                    },
        {"strip": {"fields": "*"}},
        {"strip": {"arguments": ["+1-"], "fields": ["Phone 1", "Phone 2"]}},
        {"upper": {"fields": ["Email", "Last Name", "First Name"]}}
    ],
    "Source": {
        "argument": "filepath",
        "type": "str",
        "encoding": "utf-8",
        "format": "csv",
        "delimiter": ","
    },
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
}
```

Above sample is not all-inclusive.  Detamaps, source data, and output expect full chain of custody.  No security guarantees are made. Users are advised not to use untrusted, or malformed data.

## License

`detakon` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
