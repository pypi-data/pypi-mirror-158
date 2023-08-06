# datels

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/datels?style=plastic)](https://github.com/joe-yama/datels) [![PyPI - License](https://img.shields.io/pypi/l/datels?style=plastic)](https://github.com/joe-yama/datels) [![PyPI](https://img.shields.io/pypi/v/datels?style=plastic)](https://pypi.org/project/datels/)

`datels` is a simple CLI that displays a list of dates line by line.

## Installation

To install datels with pip, run: `pip install datels`

To install datels from source, first clone the repository and then run:
`python setup.py install`

## Basic Usage

```bash
$ datels 1994-03-07 1994-03-10
1994/03/07
1994/03/08
1994/03/09
1994/03/10
```

if you want to specify formatting,

```bash
$ datels 1994-03-07 1994-03-10 --sep="-"
1994-03-07
1994-03-08
1994-03-09
1994-03-10

$ datels 1994-03-07 1994-03-10 --format "%c"
Mon Mar  7 00:00:00 1994
Tue Mar  8 00:00:00 1994
Wed Mar  9 00:00:00 1994
Thu Mar 10 00:00:00 1994
```

The strftime to parse time, eg “%Y/%m/%d”. See strftime documentation for more information: https://docs.python.org/3/library/datetime.html#strftime-and-strptime-behavior.
