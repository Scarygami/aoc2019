import os
import sys
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from lib import intcode

def load_input(filename):
    with open(filename, "r") as file:
        inputs = [int(line) for line in file]

    # Add an extra input so the Intcode program knows when to stop reading
    inputs.append(0)
    return inputs

code = intcode.read_intcode(os.path.join(currentdir, "01.ic"))
inputs = load_input(os.path.join(currentdir, "testinput.txt"))
intcode.run_intcode(code, inputs)

inputs = load_input(os.path.join(currentdir, "input.txt"))
intcode.run_intcode(code, inputs)
