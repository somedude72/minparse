## Overview

This package is a minimal argument parsing system to get stuff done. The entire package is around 500 lines of code not counting comments or documentation, so it is very lightweight. The following features are supported:

 - Positional arguments: values provided without flags
 - Optional arguments: values provided with flags, such as `-h`, `--help`
 - Automatic help and usage text generation
 - Easy and natural parser configuration
 - ...and more (see below for details)

To install, use `pip` or your favorite PyPi package manager:

```bash
$ python -m pip install minparse
```

## Basic Example

Let's write a script using `minparse` that simply prints a greeting message to the user. We'll expect the user to supply their first and last name as command line arguments. We'll also support some flags such as `-h`/`--help` to display a help message, and `-f`/`--formal` to enable a formal greeting. Full examples can be found in the `demo` folder

Before `minparse` can read arguments from the command line, we must configure it via [`minparse.config()`](https://github.com/somedude72/minparse/blob/13c9e8356599a7e3f306aa2e6c63b22dccf8ca19/src/minparse/parser.py#L36). 

```py
import minparse

config = minparse.config()
config.positional_args = ["first", "last"]
config.optional_args = {
    "help"   : (minparse.BIN, "-h", "--help", "Displays the help message and quits"),
    "formal" : (minparse.BIN, "-f", "--formal", "Make the greeting message fancy")
}
```

In this config, we register two positional arguments, which we name `first` and `last`. We also register two optional arguments, which we name `help` and `formal`. Observe how the config format is similar to a help message. This is one of `minparse`'s advantages: having a more semantically natural config. 

Notice that each optional argument has four settings that we can tweak: 

 - a [value type](https://github.com/somedude72/minparse/blob/13c9e8356599a7e3f306aa2e6c63b22dccf8ca19/src/minparse/types.py#L16) (for example, `minparse.BIN` for binary flags),
 - a short command line flag that triggers the optional argument (for example, `-h`),
 - a long command line flag that triggers the optional argument (for example, `--help`),
 - a description.

Next, we can parse the command line arguments using [`minparse.parse_arguments()`](https://github.com/somedude72/minparse/blob/13c9e8356599a7e3f306aa2e6c63b22dccf8ca19/src/minparse/parser.py#L85). This automatically reads and parses from the contents of `sys.argv`, and stores the result in [`minparse.result()`](https://github.com/somedude72/minparse/blob/13c9e8356599a7e3f306aa2e6c63b22dccf8ca19/src/minparse/parser.py#L67). We can retrieve from the results like demonstrated below:

```py
minparse.parse_arguments()

result = minparse.result()
first  = result.positional_args["first"]
last   = result.positional_args["last"]
help   = result.optional_args["help"]
formal = result.optional_args["formal"]
```

By default, parsed values are stored as strings. If an optional argument is declared with a different value type, such as `minparse.INT` or `minparse.BIN`, the stored value is automatically converted to an `int` or `bool` respectively (alternatively, an [error](#error-handling) may be raised if the conversion fails). 

If an argument is not supplied on the command line, its value is a falsy default (`""`, `False`, or `0`). This makes presence checks straightforward and avoids additional validation boilerplate. For example, we can finish our script with the following code: 

```py
greeting = "Hello"

if formal:
    greeting += " Dr."
if first:
    greeting += " " + first
if last:
    greeting += " " + last

if help:
    print("Usage: script.py [first] [last] [-h | --help] [-f | --formal]")
    print("This is a script demo for the minparse library")
else:
    print(greeting + "!")
```

Let's do some test runs with our example script. 

```
$ python script.py John Doe
Hello John Doe!
```

```
$ python script.py -f Mary
Hello Dr. Mary!
```

```
$ python script.py Walker --formal Young
Hello Dr. Walker Young!
```

```
$ python script.py Patricia Clark --help
Usage: script.py [first] [last] [-h | --help] [-f | --formal]
This is a script demo for the minparse library
```

### Help Messages

You may have noticed that we manually printed the usage message in the example above. This can be less than optimal, especially if the command line interface is complex. Therefore, `minparse` also supports automatic usage and help messages, which are synthesized directly from the config. We can access them like so:

```py
result     = minparse.result()
help_text  = result.generated_help
usage_text = result.generated_usage

print(help_text) # Help text starts with usage text
```

For our example above, this would print the following:

```
Usage: demo.py [options ...] [first] [last] 

Options: 
  -h --help     Displays the help message and quits
  -f --formal   Make the greeting message fancy
```

A line of help text will be generated for each optional argument, unless you specify `None` in place of the description of that optional argument. In that case, `minparse` will display that optional in the usage text instead. 

You can also specify the preamble and postamble text to be inserted into the help message. Everything will be rewrapped to terminal width, and all whitespaces will be shortened to a single space. To start a new paragraph in the help text, use two consecutive new lines. 

### Varidic Positionals

The parser also supports positional arguments that take an arbitrary number of values. These are aptly named varidic positionals (naming inspired by the [programming concept](https://en.wikipedia.org/wiki/Variadic_function#)). To declare it, place an ellipsis (`...`) at the end of the `positional_args` list.

```py
parser.config().positional_args = ["first", "last", ...]
```

The configuration above will turn the positional named `last` varidic. 

Instead of storing a single string, it collects all remaining command line arguments and stores them as a list of strings. The preceding positional arguments continue to behave normally and must be satisfied before the variadic positional begins absorbing values. 

### Error Handling

This library does not terminate your script on your behalf similar to other libraries (such as [argparse](https://docs.python.org/3/library/argparse.html)). If an error occurs during argument parsing, you must catch it yourself. This is by design and gives you more control. 

There are two error classes in total: 

 - [`minparse.ParserConfigError`](https://github.com/somedude72/minparse/blob/13c9e8356599a7e3f306aa2e6c63b22dccf8ca19/src/minparse/types.py#L113): If there are any config errors, this will be raised to warn the developer in advance.
 - [`minparse.ParserResultError`](https://github.com/somedude72/minparse/blob/13c9e8356599a7e3f306aa2e6c63b22dccf8ca19/src/minparse/types.py#L117): If the command line arguments supplied to the parser are malformed, this will be raised.

Both error classes contain helpful error messages to the developer and the user respectively. As an example, you can use the following snippet to handle errors during argument parsing: 

```py
try:
    minparse.parse_arguments()
except minparse.ParserResultError as e:      # Note: The help and usage texts
    print(minparse.result().generated_usage) # will be generated properly
    print(str(e))                            # even if the parsing fails. 
    return
```

### Addendums

The following additional features are supported:
 - GNU-style stacked flags: the flag `-abc` is equivalent to `-a -b -c`
 - Standard double hyphen '`--`' for stopping optional arguments parsing

The following features are not supported:
 - No stacked flags with arguments: the flag `-abcValue` is not equal to `-a -b -c Value`
 - No varidic optional flags: optional flags may take only zero or one arguments
 - No record of the count and locations of optional flags: If an optional was specified multiple times, only the last will take precedence

## Support

Consider starring this repository to support the project. 