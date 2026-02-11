"""Do not import this file or use the symbols it defines by itself. This file
defines the internal business logic that minparse uses. All public symbols are
imported via `import minparse` and can be retrieved via `minparse.__all__`. 
"""

import os
import re
import sys
import textwrap

from types import EllipsisType

from .types import (
    BIN, 
    STR, 
    INT,
    ParserConfig, 
    ParserResult, 
    ParserConfigError, 
    ParserUserError
)

__all__ = [
    "config",
    "result",
    "generate_help",
    "parse_arguments"
]


# ==========
# Variables
# ==========

# These are accessed through functions because docstrings are cool. 
_config: ParserConfig = ParserConfig()
_result: ParserResult = ParserResult()


def config() -> ParserConfig:
    """Configuration for the argument parser and auto help generator.

    A positional argument is identified by its position whereas an optional
    argument is specified by a flag and optionally accepts values (e.g. --list). 
    
    :positional_args: A list of string representing the unique name of that
        positional argument. The last list element may be ellipsis (...) to
        signify that the second to last list element takes in a varidic
        number of arguments. 

    :optional_args: A dictionary that maps the keys of the optionals to tuples
        with indices specifying the type of argument to take, the short flag,
        the long flag, and the help text. 

        The type of arguments allowed can either be `BIN`, `STR`, or `INT`. The
        help text and either the short or the long flag may be set to None. If
        the help text is none, the optional flag will not have a line in the
        auto-generated help text.

        The short and the long flag must be unique over all optionals. 

    :program_name: The name of the program to show in the generated usage text

    :help_preamble: A short description to print immediately before the help. 

    :help_postamble: A short description to print immediately after the help. 
    """
    return _config


def result() -> ParserResult:
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
    return _result


# ===============
# Initialization
# ===============

def _check_config_integrity():
    # Attempt to catch any errors in configuration so that the parser will not
    # crash to do, for example, bad variable types in the config. 
    pos_conf = _config.positional_args
    opt_conf = _config.optional_args

    seen_positional = set()
    for i, conf in enumerate(pos_conf):
        if conf in seen_positional:
            raise ParserConfigError(
                f"The name of each positional must be unique: the name "
                f"'{conf}' has been used multiple times in the config. ")
        if i != len(pos_conf) - 1 and conf == Ellipsis:
            raise ParserConfigError(
                f"Ellipsis can only be the last list element of the "
                f"positionals config: list element {i}, which is not the "
                f"last list element, cannot be ellipsis. ")
        if i == len(pos_conf) - 1 and type(conf) not in [str, EllipsisType]:
            raise ParserConfigError(
                f"Each positional name must be a string: the last "
                f"positional '{conf}' is not a string or ellipsis. ")
        if i != len(pos_conf) - 1 and type(conf) is not str:
            raise ParserConfigError(
                f"Each positional name must be a string: "
                f"the name '{conf}' is not a string. ")
        seen_positional.add(conf)
    
    seen_short_flags = set()
    seen_long_flags = set()
    for arg, conf in opt_conf.items():
        if type(arg) is not str:
            raise ParserConfigError(
                f"Each optional key must be a string: "
                f"the optional '{arg}' is not a string. ")
        if len(conf) != 4:
            raise ParserConfigError(
                f"Each optional configuration must be a tuple with four "
                f"elements: that is not the case for the '{arg}' optional. ")
        if conf[0] not in [BIN, INT, STR]:
            raise ParserConfigError(
                f"The zeroth index of each optionals config must be either "
                f"BINARY_ONLY, NUMBER_ONLY, or STRING_ONLY: that is not the "
                f"case for the '{arg}' optional. ")
        if type(conf[1]) not in [str, type(None)] or \
           type(conf[2]) not in [str, type(None)]:
            raise ParserConfigError(
                f"Each optional arguments must be a string: the flags "
                f"for the optional '{arg}' is not a string. ")
        if conf[1] is None and conf[2] is None:
            raise ParserConfigError(
                f"Either the short flag or the long flag for the optionals "
                f"config must not be None: both flags are set to None for "
                f"the '{arg}' optional. ")
        if conf[1] and len(conf[1]) != 2:
            raise ParserConfigError(
                f"Short optional flags must be two characters long (e.g. -h, -v): "
                f"that is not the case for the '{arg}' optional. ")
        if (conf[1] and len(conf[1]) == 2 and not (conf[1][0] == "-")) or \
           (conf[2] and len(conf[2]) >= 3 and not (conf[2][0] == "-" and conf[2][1] == "-")):
            raise ParserConfigError(
                f"Short optional flags must start with '-', and long optional flags "
                f"must start with '--': that is not the case for the '{arg}' optional. ")
        if (conf[1] and conf[1] in seen_short_flags) or \
           (conf[2] and conf[2] in seen_long_flags):
            raise ParserConfigError(
                f"The flag of each optional must be unique: the flags "
                f"for the optional '{arg}' has been used multiple times. ")
        if type(conf[3]) not in [str, type(None)]:
            raise ParserConfigError(
                f"Each help message must be a string: the help message "
                f"for the optional '{arg}' is not a string. ")
        seen_short_flags.add(conf[1])
        seen_short_flags.add(conf[2])

    if type(_config.program_name) not in [str, type(None)]:
        raise ParserConfigError(f"The program name must be of str type (or None)")
    if type(_config.help_preamble) not in [str, type(None)]:
        raise ParserConfigError(f"The help preamble must be of str type (or None)")
    if type(_config.help_postamble) not in [str, type(None)]:
        raise ParserConfigError(f"The help postamble must be of str type (or None)")


def _initialize_result(result):
    pos_conf = _config.positional_args
    opt_conf = _config.optional_args

    for arg in pos_conf:
        result._positional_args[arg] = ""
    if pos_conf and pos_conf[-1] is Ellipsis:
        result._positional_args[pos_conf[-2]] = []
        del result._positional_args[Ellipsis]

    for arg, conf in opt_conf.items():
        if conf[0] is BIN:
            result._optional_args[arg] = False
        if conf[0] is INT:
            result._optional_args[arg] = 0
        if conf[0] is STR:
            result._optional_args[arg] = ""


# =====================
# Help text generation
# =====================

def _get_safe_term_width():
    SAFE_AREA_CHARS = 2
    width = os.get_terminal_size().columns
    return width - SAFE_AREA_CHARS


def _long_flag_with_tail(conf):
    type = conf[0]
    tail = " <str>" if type is STR else ""
    tail = " <int>" if type is INT else tail
    return conf[2] + tail


def _wrap_help_line(text, indent):
    text = text.replace("\n", "")
    text = textwrap.fill(text, width=_get_safe_term_width() - indent)
    text = text.replace("\n", "\n" + " " * indent)
    return text


def _wrap_help_ambles(text):
    # Note: ChatGPT generated. The pattern matches one linebreak followed by one
    # or more additional linebreaks (CR, LF, or CRLF) possibly separated by
    # intermediate whitespace. 
    pattern = re.compile(r'(?:\r\n?|\n)(?:[ \t\f\v]*(?:\r\n?|\n))+')
    text = pattern.sub("\n\n", text)
    text = text.split("\n\n")
    text = [textwrap.fill(seg, width=_get_safe_term_width()) for seg in text]
    text = "\n\n".join(text)
    return text


def _generate_usage(pos_conf, opt_conf, program):
    usage = ["Usage: " + program]

    if opt_conf:
        usage[0] += " [options ...] "

    # Short flag generation
    short_flags = ""
    for _, conf in opt_conf.items():
        if not conf[3] and conf[1]:
            short_flags += conf[1][1]
    if short_flags:
        usage[0] += "[-" + short_flags + "] "

    # Long flag generation with line wrap
    long_flags = []
    for _, conf in opt_conf.items():
        if not conf[3] and not conf[1]:
            flag = _long_flag_with_tail(conf)
            long_flags.append("[" + flag + "] ")
    while long_flags:
        if len(usage[-1] + long_flags[0]) >= 80:
            usage.append(" " * len("Usage: "))
        usage[-1] += long_flags[0]
        long_flags = long_flags[1:]
    
    # Positionals generation with line wrap
    if pos_conf and pos_conf[-1] is Ellipsis:
        pos_conf.pop()
        pos_conf[-1] += " ..."
    for arg in pos_conf:
        if len(usage[-1] + arg) + 3 >= 80:
            usage.append(" " * len("Usage: "))
        usage[-1] += "[" + arg + "] "
    usage[-1] += "\b"
    return "\n".join(usage)


def _generate_opt_lines(opt_conf):
    if not opt_conf:
        return []

    opt_lines = []
    col_2_beg = 5
    col_3_beg = 3 + col_2_beg + max(
        len(_long_flag_with_tail(conf) or [])
        for _, conf in opt_conf.items())

    for _, conf in opt_conf.items():
        line = ""
        short = conf[1]
        long = conf[2]
        text = conf[3]
        if not text:
            continue

        if short:
            line += " " * 2 + short + " "
        else:
            line += " " * col_2_beg
        if long:
            long = _long_flag_with_tail(conf)
            line += long + " " * (col_3_beg - col_2_beg - len(long))
        else:
            line += " " * (col_3_beg - col_2_beg)

        line += _wrap_help_line(text, col_3_beg)
        opt_lines.append(line)

    return opt_lines


def generate_help():
    """Generates the help and usage messages for the program according to
    `minparse.Config`. This function populates the `generated_usage` and
    `generated_help` attributes in the `minparse.Result` object. 
    """

    global _result
    _check_config_integrity()
    
    program = _config.program_name or os.path.basename(sys.argv[0])
    pos_conf = _config.positional_args.copy()
    opt_conf = _config.optional_args.copy()
    preamble = _config.help_preamble
    postamble = _config.help_postamble
    
    usage = _generate_usage(pos_conf, opt_conf, program)
    opt_lines = _generate_opt_lines(opt_conf)
    help = usage

    if preamble:
        help += "\n\n" + _wrap_help_ambles(preamble)
    if opt_lines:
        help += "\n\nOptions: \n" + "\n".join(opt_lines)
    if postamble:
        help += "\n\n" + _wrap_help_ambles(postamble)

    _result._generated_usage = usage
    _result._generated_help = help


# =============
# Flag parsing
# =============

def _is_regular_flag(flag):
    return flag[0] == "-" and not _is_stacked_flag(flag)


def _is_stacked_flag(flag):
    return len(flag) >= 3  \
        and flag[0] == "-" \
        and flag[1] != "-"


def _get_flag_name(arg):
    # Returns the programmatic name of the flag from an argument, or otherwise
    # None if the flag does not exist. 
    opt_flags = _config.optional_args
    return next((
        name for name, conf in opt_flags.items()
        if conf[1] == arg or conf[2] == arg), None)


def _next_positional_parser(result, args_left, pos_conf):
    arg = args_left[0]
    if not pos_conf:
        raise ParserUserError(
            f"Too many arguments: unexpected "
            f"positional '{arg}' received. ")
    
    name = pos_conf[0]
    pos_result = result._positional_args
    if len(pos_conf) == 2 and pos_conf[1] is Ellipsis:
        pos_result[name].append(arg)
        args_left[:] = args_left[1:]
        # Note: The [:] is necessary here to operate on the referenced list,
        # as opposed to reassigning the local args_left variable, so that the
        # caller sees the change. Disclaimer: ChatGPT came up with this. 
    else:
        pos_result[name] = arg
        args_left[:] = args_left[1:]
        pos_conf[:] = pos_conf[1:]


def _next_regular_flag_parser(result, args_left, opt_conf):
    arg = args_left[0]
    name = _get_flag_name(arg)
    if not name:
        raise ParserUserError(
            f"Invalid flag received: option '{arg}' "
            f"is not a valid argument. ")
    
    tp = opt_conf[name][0]
    opt_result = result._optional_args

    if tp is BIN:
        opt_result[name] = True
        args_left[:] = args_left[1:]
        return
    
    if len(args_left) >= 3 and args_left[1] == "=":
        opt_result[name] = args_left[2]
        args_left[:] = args_left[3:]
    elif len(args_left) >= 2 and args_left[1] != "=":
        opt_result[name] = args_left[1]
        args_left[:] = args_left[2:]
    else:
        raise ParserUserError(
            f"Bad formatting: mission argument "
            f"for option '{arg}'. ")
    
    if tp is INT:
        if opt_result[name].isdigit():
            opt_result[name] = int(opt_result[name])
        else:
            raise ParserUserError(
                f"Bad formatting: only integers "
                f"argument allowed for option '{arg}'. ")


def _next_stacked_flag_parser(result, args_left, opt_conf):
    arg = args_left[0]

    for char in arg[1:]:
        unstacked_flag = "-" + char

        name = _get_flag_name(unstacked_flag)
        if not name:
            raise ParserUserError(
                f"Invalid flag received: option '{unstacked_flag}' "
                f"(in '{arg}') is not a argument. ")

        tp = opt_conf[name][0]
        if tp is not BIN:
            raise ParserUserError(
                f"Bad formatting: option '{unstacked_flag}' "
                f"(in '{arg}') cannot be stacked. ")
        
        result_storage = result._optional_args
        result_storage[name] = True
    args_left[:] = args_left[1:]


def _split_equal_sgn(args):
    result = []
    for arg in args:
        if arg == "=":
            raise ParserUserError(f"Bad formatting: unexpected floating '=' sign. ")
        if "=" in arg:
            result.append(arg.split("=")[0])
            result.append("=")
            result.append(arg.split("=")[1])
        else:
            result.append(arg)
    return result


def parse_arguments() -> None:
    """Parse command line arguments using the config provided by
    `minparse.Config`. This function populates the `positional_args` and
    `optional_args` attributes in the `minparse.Result` object. 
    """
    global _result
    _check_config_integrity()
    _initialize_result(_result)

    args_left = sys.argv[1:]
    pos_config = _config.positional_args.copy()
    opt_config = _config.optional_args.copy()
    args_left = _split_equal_sgn(args_left)
    no_more_optionals = False

    while args_left:
        # Note: The following helper functions only parses the 0th args_left and
        # deletes everything that's already been parsed. This is why the loop
        # does not end until args_left is empty.
        if args_left[0] == "--":
            no_more_optionals = True
            args_left = args_left[1:]
            continue

        if no_more_optionals:
            _next_positional_parser(_result, args_left, pos_config)
        elif _is_regular_flag(args_left[0]):
            _next_regular_flag_parser(_result, args_left, opt_config)
        elif _is_stacked_flag(args_left[0]):
            _next_stacked_flag_parser(_result, args_left, opt_config)
        else:
            _next_positional_parser(_result, args_left, pos_config)