import sys

from ctr.bclyt import Bclyt
from ctr.msbp import Msbp

# Get arguments from command line
args = sys.argv[1:]

# Check if there are any arguments
if len(args) == 0:
    print("Usage: python unpack.py <bclyt|msbp> <file> [<output>]")
    exit()

# Unpack the file based on the arguments
match args[0]:
    case "bclyt":
        if len(args) < 2:
            print("Usage: python unpack.py bclyt <file> [<output>]")
            exit()
        bclyt = Bclyt(args[1])
    case "msbp":
        if len(args) < 2:
            print("Usage: python unpack.py msbp <file.msb> [<output.json>]")
            exit()
        msbp = Msbp(args[1])
        msbp.to_json(args[2])
    case _:
        print("Usage: python unpack.py <bclyt|msbp> <file> [<output>]")
