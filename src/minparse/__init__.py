"""
### Overview

This package is a minimal argument parsing system to get stuff done. The entire
package is around 500 lines of code not counting comments or documentation, so
it is very lightweight. The following features are supported:

- Positional arguments: values provided without flags
- Optional arguments: values provided with flags, such as `-h`, `--help`
- Automatic help and usage text generation
- Easy and natural parser configuration
- ...and more (see below for details)

### Basic Example

Let's write a script using `minparse` that simply prints a greeting message to
the user. We'll expect the user to supply their first and last name as command
line arguments. We'll also support some flags such as `-h`/`--help` to display a
help message, and `-f`/`--formal` to enable a formal greeting. Full examples can
be found in the `demo` folder

Before `minparse` can read arguments from the command line, we must configure it
via `minparse.config()`:

```
import minparse

config = minparse.config()
config.positional_args = ["first", "last"]
config.optional_args = {
    "help"   : (minparse.BIN, "-h", "--help", "Displays the help message"),
    "formal" : (minparse.BIN, "-f", "--formal", "Make the greeting formal")
}
```

In this config, we register two positional arguments, which we name `first` and
`last`. We also register two optional arguments, which we name `help` and
`formal`. Observe how the config format is similar to a help message. This is
one of `minparse`'s advantages: having a more semantically natural config. 

Notice that each optional argument has four settings that we can tweak: 

- a value type
- a short command line flag that triggers the optional (for example, `-h`),
- a long command line flag that triggers the optional (for example, `--help`),
- a description.

Next, we can parse the command line arguments using
`minparse.parse_arguments()`. This automatically reads and parses from the
contents of `sys.argv`, and stores the result in `minparse.result()`. We can
retrieve from the results like demonstrated below:  

```
minparse.parse_arguments()

result = minparse.result()
first  = result.positional_args["first"]
last   = result.positional_args["last"]
help   = result.optional_args["help"]
formal = result.optional_args["formal"]
```

By default, parsed values are stored as strings. If an optional argument is
declared with a different value type, such as `minparse.INT` or `minparse.BIN`,
the stored value is automatically converted to an `int` or `bool` respectively
(alternatively, an error may be raised if the conversion fails). 

If an argument is not supplied on the command line, its value is a falsy default
(`""`, `False`, or `0`). This makes presence checks straightforward and avoids
additional validation boilerplate. For example, we can finish our script with
the following code:  

```
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
"""

from .parser import config, result, parse_arguments
from .types import (
    ParserConfig, 
    ParserResult, 
    ParserConfigError, 
    ParserResultError, 
    BIN, 
    STR, 
    INT
)

__all__ = [
    "config",
    "result",
    "parse_arguments",
    "ParserConfig",
    "ParserResult",
    "ParserConfigError",
    "ParserResultError",
    "BIN",
    "STR",
    "INT",
]