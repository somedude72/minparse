"""
This package is a minimal argument parsing system to get stuff done.

Before `minparse` can read arguments from the command line, you must tell it
which arguments to expect. This is done by configuring it. 

 - Positional arguments: values that are provided without flags
 - Optional arguments: values that are provided with flags (e.g. -h, --help)

You can use the following example to configure the parser. 

```
    parser.config().program_name = "demo.py"
    parser.config().help_preamble = \"\"\"\\
    This preamble will get rewrapped to
    terminal width, so the linebreaks here
    won't show up in the actual help text!
    However, two or more linebreaks like
    the following will result in a new
    paragraph after rewrapping.

    The following options configuration simulates a simplified grep cli, and serves
    as a quick demonstration of the capabilities of minparse. 
    \"\"\"
    parser.config().help_postamble = \"\"\"\\
    This demonstration file will be necessarily incomplete in showcasing the full
    features and logic of the argument parsing system. To learn more, visit the
    GitHub repo at https://github.com/somedude72/minparse for details. 
    \"\"\"

    parser.config().positional_args = ["pattern", "files", ...] # files is a varidic argument. 
    parser.config().optional_args = {
        "help"       : (parser.BIN, "-h", "--help", "Print the help message and quit"),
        "case"       : (parser.BIN, "-i", "--ignore-case", "Ignore case distinctions"),
        "invert"     : (parser.BIN, "-v", "--invert-match", "Select non-matching lines"),
        "word-regex" : (parser.BIN, "-w", "--word-regexp", "Match whole words only"), 
        "line-regex" : (parser.BIN, "-x", "--line-regexp", "Match whole lines only"),
        "file"       : (parser.STR, None, "--file", "Obtain patterns from FILE, one per line"), 
        "include"    : (parser.STR, None, "--include", "Search only files matching GLOB <str>"), 
        "colored"    : (parser.STR, None, "--color", "Color printing options")
    }
```

For complete documentation, visit https://github.com/somedude72/minparse/tree/main.
"""

from .parser import config, result, parse_arguments
from .types import (
    ParserConfig, 
    ParserResult, 
    ParserConfigError, 
    ParserUserError, 
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
    "ParserUserError",
    "BIN",
    "STR",
    "INT",
]