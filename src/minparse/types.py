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
    """See config() for docstring"""

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
    """See result() for docstring"""

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