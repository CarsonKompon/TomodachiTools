import sys

# We need this to import from the parent directory (in this case parent OF the parent)
sys.path.append(sys.path[0] + "\\..\\..")

# The relative imports in question
from ctr import bclyt

# Get arguments from command line
args = sys.argv[1:]

# Check if there are any arguments
if len(args) == 0:
    fileName = __file__.split("\\")[-1]
    print("Usage: python " + fileName + ".py <input_file> [<output_file>]")
    exit()

# Get input and output file from args
input_file = args[0]
output_file = input_file
if len(args) > 1:
    output_file = args[1]

# If output file isn't .json, append proper extension
if not output_file.endswith(".json"):
    output_file += ".json"


### ACTUAL SCRIPT BELOW THIS COMMENT ###
binaryLayout = bclyt.Bclyt(input_file)
json = str(binaryLayout)

with open(output_file, "w") as f:
    f.write(json)