# detakon

[![PyPI - Version](https://img.shields.io/pypi/v/detakon.svg)](https://pypi.org/project/detakon)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/detakon.svg)](https://pypi.org/project/detakon)

-----

## Table of Contents

- [Installation](#installation)
- [License](#license)

## Installation

NOTE: Currently in pre-release.  Current status is: Minimal viable product for CSV to CSV conversions only.  Not for usage in production systems.

```console
pip install detakon
```

## Detamap Files

A detamap configuration file is used to provide all details necessary for the data conversion.

A datamap must be a Python dictionary, or convertable to a Python dictionary.  Currently this means either a dictionary or JSON file (plans to add TOML support).

A detamap MUST include the following key:value pairs:
- "Fields" as a list of strings corresponding to the output field names in the desired order.
- "Mappings" with a sub-dictionary of source data field names as keys, mapped to output field names as values.
- "Defaults" with a sub-dictionary of output field names that will supply a default value if either: (not currently implemented)
    - Matching field was not found in source.
    - Matching source data was empty, such as an empty string.
- "Operations" with a sub-dictionary of operations to perform on output data: (not currently implemented)
    - Example opersations may be "upper", or "convertValue".
- "Source" with a sub-dictionary that defines the type of source being passed, and the arguments to pass to Path.open() if source is a file, or csv.DictReader if source is CSV data.
    - Required keys:
        - "argument" as type of argument being passed as the source argument to the Detakon initializer. Accepted values: "filepath".
            - "type" key may be required depending on the argument being passed.
- "Output" with a sub-dictionary that defines the type of output expected, and the arguments to pass to Path.open() if destination is a file, or csv.DictReader if output is CSV data. 

A detamap JSON file may look similar to:

```
{
    "Fields": ["External Order ID", "Last Name", "First Name", "DOB"],
    "Mappings": {
        "Invoice #": "External Order ID",
        "Client Last Name": "Last Name",
        "Client First Name": "First Name",
        "Date of Birth": "DOB"
    },
    "Defaults": {
        "DOB": "Unknown"
    },
    "Operations": {
        "upper": ["External Order ID", "Last Name", "First Name"]
    },
    "Source": {
        "argument": "filepath",
        "type": "str",
        "encoding": "utf-8",
        "format": "csv",
        "delimiter": ","
    },
    "Output": {
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

Above sample is not all-inclusive.  Detamaps, source data, and output expect full chain of custody.  No security guarantees are made in regards to untrusted or malformed data.

## License

`detakon` is distributed under the terms of the [MIT](https://spdx.org/licenses/MIT.html) license.
