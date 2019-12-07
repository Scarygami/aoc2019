import os
import sys
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from itertools import permutations
from lib import intcode

def one_run(inputfile):
    max_thruster = 0
    code = intcode.read_intcode(inputfile)
    for phases in permutations([0,1,2,3,4]):
        last_output = 0
        for phase in phases:
            inputs = [phase, last_output]
            outputs = intcode.run_intcode(code, inputs).outputs
            last_output = outputs.pop()
        if last_output > max_thruster:
            max_thruster = last_output

    return max_thruster

def feedback_loop(inputfile):
    max_thruster = 0
    code = intcode.read_intcode(inputfile)
    for phases in permutations([5,6,7,8,9]):
        done = False
        machines = []
        for phase in phases:
            machines.append(intcode.State(0, code, [phase]))
        last_output = 0
        while not done:
            # Initialise machines
            for m, machine in enumerate(machines):
                machine.inputs.append(last_output)
                result = intcode.run_intcode(machine.memory, machine.inputs, machine.ip, False, True)
                last_output = result.outputs[-1]
                machines[m] = result
                if not result.waiting:
                    done = True

        if last_output > max_thruster:
            max_thruster = last_output

    return max_thruster
        

assert one_run(os.path.join(currentdir, "testinput1.txt")) == 43210
assert one_run(os.path.join(currentdir, "testinput2.txt")) == 54321
assert one_run(os.path.join(currentdir, "testinput3.txt")) == 65210

print("Part 1: %s" % one_run(os.path.join(currentdir, "input.txt")))

assert feedback_loop(os.path.join(currentdir, "testinput4.txt")) == 139629729
assert feedback_loop(os.path.join(currentdir, "testinput5.txt")) == 18216

print("Part 2: %s" % feedback_loop(os.path.join(currentdir, "input.txt")))
