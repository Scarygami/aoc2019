import os
import sys
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from lib.intcode import IntcodeVM

code = IntcodeVM.read_intcode(os.path.join(currentdir, "input.txt"))
machine = IntcodeVM(code)

outputs = machine.run([1])
print("Part 1: %s" % outputs.pop())

outputs = machine.run([5])
print("Part 2: %s" % outputs.pop())
