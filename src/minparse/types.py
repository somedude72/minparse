"""Do not import this file or use the symbols it defines by itself. This file
defines the internal business logic that minparse uses. All public symbols are
imported via `import minparse` and can be retrieved via `minparse.__all__`. 
"""

__all__ = [
    "BIN",
    "STR",
    "INT",
    "ParserConfig",
    "ParserResult",
    "ParserConfigError",
    "ParserUserError",
]

BIN = object()
STR = object()
INT = object()


class ParserConfig:
    """Configuration for the argument parser and auto help generator.

    A positional argument is identified by its position (e.g. [file path]),
    whereas an optional argument is specified by name and optionally accepts
    values (e.g. --list). 
    
    :positional_args: A list of string representing the unique name of that
        positional argument. The last list element may be ellipsis (...) to
        signify that the second to last list element takes in a varidic
        number of arguments. 

    :optional_args: A dictionary that maps the keys of the optionals to tuples
        with indices specifying the type of argument to take, the short flag,
        the long flag, and the help text. 

        The type of arguments allowed can either be `BIN`, `STR`, or `NUM`. The
        help text and either the short or the long flag may be set to None. If
        the help text is none, the optional flag will not have a line in the
        auto-generated help text.

        The short and the long flag must be unique over all optionals. 

    :program_name: The name of the program to show in the generated usage text

    :help_preamble: A short description to print immediately before the help. 

    :help_postamble: A short description to print immediately after the help. 
    """

    def __init__(self) -> None:
        self._positional_args: list = []
        self._optional_args: dict = {}
        self._program_name: str | None = None
        self._help_preamble: str | None = None
        self._help_postamble: str | None = None


    @property
    def positional_args(self):
        return self._positional_args
    

    @property
    def optional_args(self):
        return self._optional_args
    

    @property
    def program_name(self):
        return self._program_name
    

    @property
    def help_preamble(self):
        return self._help_preamble
    

    @property
    def help_postamble(self):
        return self._help_postamble


    @positional_args.setter
    def positional_args(self, value: list):
        self._positional_args = value


    @optional_args.setter
    def optional_args(self, value: dict):
        self._optional_args = value


    @program_name.setter
    def program_name(self, value: str):
        self._program_name = value
    

    @help_preamble.setter
    def help_preamble(self, value: str):
        self._help_preamble = value


    @help_postamble.setter
    def help_postamble(self, value: str):
        self._help_postamble = value


class ParserResult:
    """Resulting parsed arguments for the program

    :positional_args: A dictionary mapping the programmatic names of the
        positionals in the config to the values parsed from cli arguments. 

    :optional_args: A dictionary mapping the programmatic names of the optional
        args in the config to the string (or boolean) values parsed from cli
        flags. 

    :generated_usage: A string consisting of the usage text. Useful for printing
        when exiting due to the user inputting an invalid optional flag. 

    :generated_help: A string consisting of both the usage text and the help. 
    """

    def __init__(self) -> None:
        self._positional_args: dict = {}
        self._optional_args: dict = {}
        self._generated_usage: str = ""
        self._generated_help: str = ""


    @property
    def positional_args(self):
        return self._positional_args
    

    @property
    def optional_args(self):
        return self._optional_args
    

    @property
    def generated_help(self):
        return self._generated_help
    

    @property
    def generated_usage(self):
        return self._generated_usage


class ParserConfigError(Exception):
    """Error for fatally incorrect config by the developer"""


class ParserUserError(Exception):
    """Error for fatally incorrect command line arguments by the user"""