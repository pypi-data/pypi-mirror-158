# ideal_ukpostcode


[![image](https://img.shields.io/pypi/v/ideal_ukpostcode.svg)](https://pypi.python.org/pypi/ideal_ukpostcode)


**package supports validating and formatting postcodes for the UK**


-   Free software: MIT license
-   Documentation: https://myselfdesai.github.io/ideal_ukpostcode
-   PyPI: https://pypi.python.org/pypi/ideal_ukpostcode   


## Introduction

package supports validating and formatting postcodes for the UK. The details of which postcodes are valid and which are the parts they consist of can be found at [wiki](https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Formatting)

## Installation

To install ideal_ukpostcode, run this command in your terminal:

```
pip install ideal_ukpostcode
```

This is the preferred method to install ideal_ukpostcode, as it will always install the most recent stable release.

If you don't have [pip](https://pip.pypa.io) installed, this [Python installation guide](http://docs.python-guide.org/en/latest/starting/installation/) can guide you through the process.

## From sources

The sources for ideal_ukpostcode can be downloaded from the Github repo.

You can clone the public repository:

```
git clone git://github.com/myselfdesai/ideal_ukpostcode
```

## Usage 

To use ideal_ukpostcode in a project:

### validate a postcode

it gives boolean result True or False
```
import ideal_ukpostcode
ideal_ukpostcode.validate("EC1A 1BB")
```

### format a postcode

format(area, district, sector, unit)
```
import ideal_ukpostcode
ideal_ukpostcode.format("EC","1A","1","BB")
```

## Test
install dev dependencies 
```
pip install -r requirements_dev.txt
```
In the root folder, execute :

    pytest

## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [giswqs/pypackage](https://github.com/giswqs/pypackage) project template.
