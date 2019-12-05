import os
import sys
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from lib import intcode

print("Use '1' as input for part 1:")
intcode.run_intcode(intcode.read_intcode(os.path.join(currentdir, "input.txt")))

print("Use '5' as input for part 2:")
intcode.run_intcode(intcode.read_intcode(os.path.join(currentdir, "input.txt")))
