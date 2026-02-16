# This demo script is a basic example of minparse, extracted from the GitHub
# README and complete with error checking. See the GitHub README for detailed
# descriptions. 

import minparse


# Configuration
config = minparse.config()
config.positional_args = ["first", "last"]
config.optional_args = {
    "help"   : (minparse.BIN, "-h", "--help", "Displays the help message and quits"),
    "formal" : (minparse.BIN, "-f", "--formal", "Make the greeting message fancy")
}

# Parsing
try:
    minparse.parse_arguments()
except minparse.ParserResultError as e:      # Note: The help and usage texts
    print(minparse.result().generated_usage) # will be generated properly
    print(str(e))                            # even though the parsing failed. 
    quit()

# Extracting
result = minparse.result()
first  = result.positional_args["first"]
last   = result.positional_args["last"]
help   = result.optional_args["help"]
formal = result.optional_args["formal"]
manual = result.generated_help

greeting = "Hello"

# Printing
if formal:
    greeting += " Dr."
if first:
    greeting += " " + first
if last:
    greeting += " " + last

if help:
    print(manual)
else:
    print(greeting + "!")