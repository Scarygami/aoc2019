import os
import sys
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from lib import intcode

def run_intcode(inputfile, noun=None, verb=None):
    """Runs the Intcode provided in inputfile

    Parameters
    ----------
    inputfile : str
        Name/path of file that contains the puzzle input

    noun : int
        Fixed value to put into memory[1]

    verb : int
        Fixed value to put into memory[2]
    """

    memory = intcode.read_intcode(inputfile)

    if noun is not None:
        memory[1] = noun
    if verb is not None:
        memory[2] = verb

    return intcode.run_intcode(memory)

result = run_intcode(os.path.join(currentdir, "input.txt"), 12, 2)
print("Part 1: %s" % (result[0]))

# Brute-forcing part 2, because too lazy to reverse-engineer the intcode
for noun in range(0, 100):
    for verb in range(0, 100):
        if run_intcode(os.path.join(currentdir, "input.txt"), noun, verb)[0] == 19690720:
            print("Part 2: %s" % (100 * noun + verb))
            exit(0)
