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


def run_sprintcode(machine, code):
    outputs = machine.run("\n".join(code))
    for output in outputs:
        if output > 255:
            return output
        else:
            print(chr(output), end="")


source = IntcodeVM.read_intcode(os.path.join(currentdir, "input.txt"))
machine = IntcodeVM(source, silent=True)

code1 = [
    "NOT A J",
    "NOT B T",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND D J",
    "WALK",
    ""
]

print("Part 1: %s" % run_sprintcode(machine, code1))

code2 = [
    "NOT A J",
    "NOT B T",
    "OR T J",
    "NOT C T",
    "OR T J",
    "AND D J",
    "NOT H T",
    "NOT T T",
    "OR E T",
    "AND T J",
    "RUN",
    ""
]

print("Part 2: %s" % run_sprintcode(machine, code2))
