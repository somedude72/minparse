# This demo script is inspired by the grep cli commands. It demonstrates how
# minparse behaves when you need a complex interface as well as some other
# features not covered in the README.

import minparse
from pprint import pprint # Pretty printing Python dictionaries


def configure_parser():
    config = minparse.config()
    config.program_name = "demo.py"
    config.help_preamble = """
    The following options configuration emulates a complex cli in minparse, and
    serves as a quick demonstration of the quirks and capabilities of minparse.

    This preamble will get rewrapped to
        terminal width, so the linebreaks here
            won't show up in the actual help text!
            However, two or more linebreaks like
        the following will result in a new
    paragraph after rewrapping.

    
    """
    config.help_postamble = "Bottom Text"

    config.positional_args = ["pattern", "files", ...] # files is a varidic argument. 
    config.optional_args = {
        "help"       : (minparse.BIN, "-h", "--help", "Print the help message and quit"),
        "case"       : (minparse.BIN, "-i", "--ignore-case", "Ignore case distinctions"),
        "invert"     : (minparse.BIN, "-v", "--invert-match", "Select non-matching lines"),
        "word-regex" : (minparse.BIN, "-w", "--word-regexp", "Match whole words only"), 
        "line-regex" : (minparse.BIN, "-x", "--line-regexp", "Match whole lines only"),
        "file"       : (minparse.STR, None, "--file", "Obtain patterns from FILE, one per line"), 
        "include"    : (minparse.STR, None, "--include", "Search only files matching GLOB <str>"), 
        "colored"    : (minparse.STR, None, "--color", "Color printing options")
    }


def main():
    try:
        configure_parser()
        minparse.parse_arguments()
    except minparse.ParserResultError as e:
        print(minparse.result().generated_usage)
        print(str(e))
        return

    if minparse.result().optional_args["help"]:
        print(minparse.result().generated_help)
    else:
        print("The program received the following:")
        pprint(minparse.result().positional_args)
        pprint(minparse.result().optional_args)


if __name__ == "__main__":
    main()