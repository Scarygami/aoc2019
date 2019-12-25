import os
import sys
from itertools import combinations
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

try:
    from lib.intcode import IntcodeVM
except ImportError:
    print("Intcode library could not be found")
    exit(1)

source = IntcodeVM.read_intcode(os.path.join(currentdir, "input.txt"))
machine = IntcodeVM(source, silent=True)

# Path to security checkpoint picking up all safe items
walkthrough = [
    "east",
    "east",
    "take semiconductor",
    "north",
    "take planetoid",
    "west",
    "take food ration",
    "west",
    "west",
    "take monolith",
    "east",
    "east",
    "north",
    "take space law space brochure",
    "east",
    "take jam",
    "west",
    "north",
    "north",
    "take weather machine",
    "south",
    "south",
    "south",
    "east",
    "north",
    "take antenna",
    "south",
    "south",
    "east",
    "south",
    "south",
    "east",
    "drop food ration",
    "drop weather machine",
    "drop antenna",
    "drop space law space brochure",
    "drop jam",
    "drop semiconductor",
    "drop planetoid",
    "drop monolith"
]

items = [
    "food ration",
    "weather machine",
    "antenna",
    "space law space brochure",
    "jam",
    "semiconductor",
    "planetoid",
    "monolith"
]


machine.run("\n".join(walkthrough) + "\n")

# Brute forcing all item combinations until the right weight is reached.
for l in range(len(items)):
    for selected in combinations(items, l):
        steps = []
        for item in selected:
            steps.append("take %s" % item)
        steps.append("east")

        outputs = machine.resume("\n".join(steps) + "\n")
        outputs = "".join([chr(c) for c in outputs])
        if outputs.find("lighter") >= 0:
            print("Too heavy:", selected)
        elif outputs.find("heavier") >= 0:
            print("Too light:", selected)
        else:
            print(outputs)
            exit()

        steps = []
        for item in selected:
            steps.append("drop %s" % item)
        machine.resume("\n".join(steps) + "\n")
