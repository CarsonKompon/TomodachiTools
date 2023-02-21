import sys
import os

from ctr.bclyt import Bclyt
from ctr.msbp import Msbp

bclyt = Bclyt("working/Clock_U.bclyt")
print(str(bclyt))

# Create a new folder
if not os.path.exists("working"):
    os.makedirs("working")
    
# Create a new file
bclyt.export("working/Clock_U_new.bclyt")