import os
import sys
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

try:
    from lib.intcode import IntcodeVM
except ImportError:
    print("Intcode library could not be found")
    exit(1)


def load_input(filename):
    with open(filename, "r") as file:
        inputs = [int(line) for line in file]

    # Add an extra zero at the end so the Intcode program knows when to stop reading
    inputs.append(0)
    return inputs


code1 = IntcodeVM.read_intcode(os.path.join(currentdir, "01_part1.ic"))
machine = IntcodeVM(code1)

print("Testcases")
outputs = machine.run([12, 0])
assert outputs.pop() == 2
outputs = machine.run([14, 0])
assert outputs.pop() == 2
outputs = machine.run([1969, 0])
assert outputs.pop() == 654
outputs = machine.run([100756, 0])
assert outputs.pop() == 33583


inputs = load_input(os.path.join(currentdir, "testinput.txt"))
outputs = machine.run(inputs)
assert outputs.pop() == 34241

print("Part 1")
inputs = load_input(os.path.join(currentdir, "input.txt"))
machine.run(inputs)
