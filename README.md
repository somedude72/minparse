## Overview

This package is a minimal argument parsing system to get stuff done. 

The main motivation behind designing yet another argument parsing system is that most argument parsing systems such as [argparse](https://docs.python.org/3/library/argparse.html), [typer](https://pypi.org/project/typer/), and [click](https://pypi.org/project/click/) all attempt to handle everything from pretty printing to exiting gracefully and more. While this can be convenient, sometimes you just want a small, reliable, and customizable argument parsing system that just does argument parsing, which is exactly what minparse is built for. 

What this library supports:

 + Positional arguments
 + Optional arguments
 + GNU-style stacked flags
 + Auto-generated usage and help text
 + ... and more! 

What this library does **not** support:

 + Custom parsers
 + Extensive error checking
 + Mutually exclusive arguments

The entire library is written in around 600 lines of code (about 400 lines not counting comments and blank lines), so it is fairly lightweight. 

## Installation

To install, use the `pip` package manager:

```sh
$ python -m pip install minparse
```

## Tutorial

Under construction

## Support

Consider starring this repository to support the project. 