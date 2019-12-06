import os
import sys
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from lib import intcode

def load_input(filename):
    with open(filename, "r") as file:
        inputs = [int(line) for line in file]

    # Add an extra zero at the end so the Intcode program knows when to stop reading
    inputs.append(0)
    return inputs

code1 = intcode.read_intcode(os.path.join(currentdir, "01_part1.ic"))

print("Testcases")
_, outputs = intcode.run_intcode(code1, [12, 0])
assert outputs.pop() == 2
_, outputs = intcode.run_intcode(code1, [14, 0])
assert outputs.pop() == 2
_, outputs = intcode.run_intcode(code1, [1969, 0])
assert outputs.pop() == 654
_, outputs = intcode.run_intcode(code1, [100756, 0])
assert outputs.pop() == 33583


inputs = load_input(os.path.join(currentdir, "testinput.txt"))
_, outputs = intcode.run_intcode(code1, inputs)
assert outputs.pop() == 34241

print("Part 1")
inputs = load_input(os.path.join(currentdir, "input.txt"))
intcode.run_intcode(code1, inputs)
