import sys

from ctr.bclyt import Bclyt

# Get arguments from command line
args = sys.argv[1:]

# Unpack the file based on the arguments
match args[0]:
    case "bclyt":
        if len(args) < 2:
            print("Usage: python unpack.py bclyt <file> [<output>]")
            exit()
        bclyt = Bclyt(args[1])
            