"""TODO: Write docstring"""

from .parser import Config, Result, parse_arguments, generate_help
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
    "Config",
    "Result",
    "generate_help",
    "parse_arguments",
    "ParserConfig",
    "ParserResult",
    "ParserConfigError",
    "ParserUserError",
    "BIN",
    "STR",
    "INT",
]