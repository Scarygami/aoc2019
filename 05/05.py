import os
import sys
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from lib import intcode

_, outputs = intcode.run_intcode(intcode.read_intcode(os.path.join(currentdir, "input.txt")), [1])
print("Part 1: %s" % outputs.pop())

_, outputs = intcode.run_intcode(intcode.read_intcode(os.path.join(currentdir, "input.txt")), [5])
print("Part 2: %s" % outputs.pop())
