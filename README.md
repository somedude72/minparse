## Overview

This package is a minimal argument parsing system to get stuff done. The entire library is around 500 lines of code not counting comments or documentation, so it is very lightweight. To install, use the `pip` package manager:

```bash
$ python -m pip install minparse
```

## Tutorial

Before `minparse` can read arguments from the command line, you must tell it which arguments to expect. This is done by [configuring](https://github.com/somedude72/minparse/blob/970469ea667c830674ebfde9014372789f938a2f/src/minparse/types.py#L21):

 - Positional arguments: values that are provided without flags
 - Optional arguments: values that are provided with flags (e.g. `-h`, `--help`)

You can get started using the following minimal example. 

```py
import minparse as parser

parser.config().positional_args = ["first", "last"]
parser.config().optional_args = {
    "help"    : (minparse.BIN, "-h", "--help", "Print the help message and quit"),
    "verbose" : (minparse.BIN, "-v", "--verbose", "Make the program talk more")
}

parser.parse_arguments()
print(parser.result().positional_args)
print(parser.result().optional_args)
```

For a more complete and complex example, see `demo/demo.py`. 

### Positional Arguments

Positional arguments are defined as a list of unique names as it appear in your code. Values are assigned based on their order on the command line. For example, if we use the command below to run the script above, the parser will map `first` to `Bob`, and map `last` to `Smith`. 

```bash
python script.py Bob Smith
```

When using the command line, positional arguments can be intertwined with optional arguments and flags, and will be correctly ingested by the parser. To switch off optionals parsing on the command line, the parser supports the standard '`--`' notation; all arguments after '`--`' will be parsed as positional arguments. 

### Optional Arguments

Optional arguments are defined as a dictionary. Each key is the argument’s unique name as it appears in your code, and each value describes how the argument behaves. Specifically, each value is a tuple of four elements that describes: 

 - a value type (for example, `minparse.BIN` for on/off flags),
 - a short command line flag (for example, `-h`)
 - a long command line flag (for example, `--help`)
 - a help description.

The value type can either be `minparse.BIN`, `minparse.INT`, or `minparse.STR`. If the command line arguments supply a different value type, an error will be raised (see the [errors](#errors) section). In addition, either the short flag or the long flag (but not both) may be set to `None`. The help text may also be set to `None`, in which case the optional argument will not have a line in the auto-generated help text. 

When using the command line, you can specify values via any of the following ways: `--flag value`, `--flag=value`, `-f value`, `-f=value` (you cannot, however, do `--flag = value`). Further, you can also specify GNU-style stacked flags such as `-abc`. However, the parser does not support stacked flags that consume arguments. This implies that you can only stack on/off flags. 

### Advanced

The parser supports automatic help message generation. For each optional that has help text, `minparse` will generate a line of help text for it. For each optional that does not have help text, `minparse` will generate an element in the usage text. You can also specify the preamble and postamble text to be inserted into the help message. Everything will be rewrapped to terminal width, and all whitespaces will be replaced. To start a new paragraph in the help text, use two line breaks (similar to markdown). 

The usage text and the help text can be accessed like so:

```py
# ...
parser.result().usage_text
parser.result().help_text
# ...
```

The parser also supports varidic positional arguments (positionals that take an arbitrary number of values). Only the final positional argument can be varidic; to turn the positional at the end a varidic positional, insert an ellipsis (`...`) at the end of the list. 

```py
# ...
parser.config().positional_args = ["first", "last", ...]
parser.config().optional_args = {
# ...
```

The configuration above will turn the positional named `last` varidic and map it to a list of strings from the command line. 

### Errors

There are two error classes in total: 

 - `minparse.ParserConfigError`: If there are any errors with the config, `minparse` will warn the developer in advance by raising this.
 - `minparse.ParserUserError`: If the command line arguments supplied to the parser are malformed, `minparse` will raise this.

Both error classes contain helpful error messages to the developer and the user respectively. Note that when `minparse` encounters malformed command line arguments, it **will only raise an error and will not terminate your script on your behalf** (like [argparse](https://docs.python.org/3/library/argparse.html) does). Thus, it is a good idea to catch minparse's errors and print the contents out. See `demo/demo.py` to see an example. 

### Addendums

If a position or an optional flag is not supplied by the command line arguments, the parser will assign it a falsy value (e.g. empty string, empty list, 0, False). If an optional was specified multiple times by the user, the last time will take precedence (the parser does not keep track of how many times an optional argument is specified). 

## Support

Consider starring this repository to support the project. 