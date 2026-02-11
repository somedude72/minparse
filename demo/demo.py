import minparse

from pprint import pprint


minparse.Config.program_name = "demo.py"
minparse.Config.help_preamble = """\
This preamble will get rewrapped to
terminal width, so the linebreaks here
won't show up in the actual help text!
However, two or more linebreaks like
the following will result in a new
paragraph after rewrapping.

The following options configuration simulates a simplified grep cli, and serves
as a quick demonstration of the capabilities of minparse. 
"""
minparse.Config.help_postamble = """\
This demonstration file will be necessarily incomplete in showcasing the full
features and logic of the argument parsing system. To learn more, visit the
GitHub repo at https://github.com/somedude72/minparse for details. 
"""

minparse.Config.positional_args = ["pattern", "files", ...] # files is a varidic argument. 
minparse.Config.optional_args = {
    "help"       : (minparse.BIN, "-h", "--help", "Print the help message and quit"),
    "case"       : (minparse.BIN, "-i", "--ignore-case", "Ignore case distinctions"),
    "invt"       : (minparse.BIN, "-v", "--invert-match", "Select non-matching lines"),
    "word-regex" : (minparse.BIN, "-w", "--word-regexp", "Match whole words only"), 
    "line-regex" : (minparse.BIN, "-x", "--line-regexp", "Match whole lines only"),
    "file"       : (minparse.STR, None, "--file", "Obtain patterns from FILE, one per line"), 
    "include"    : (minparse.STR, None, "--include", "Search only files matching GLOB (e.g., --include='*.py')"), 
    "colored"    : (minparse.STR, None, "--color", "Color printing options")
}


def main():
    try:
        minparse.generate_help()
        minparse.parse_arguments()
    except minparse.ParserUserError as e:
        print(minparse.Result.generated_usage)
        print(str(e))
        return

    if minparse.Result.optional_args["help"]:
        print(minparse.Result.generated_help)
    else:
        pprint(minparse.Result.positional_args)
        pprint(minparse.Result.optional_args)


if __name__ == "__main__":
    main()