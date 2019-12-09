import os
import sys
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from itertools import permutations
from lib.intcode import IntcodeVM

def one_run(inputfile):
    max_thruster = 0
    code = IntcodeVM.read_intcode(inputfile)
    machine = IntcodeVM(code)
    for phases in permutations([0,1,2,3,4]):
        last_output = 0
        for phase in phases:
            inputs = [phase, last_output]
            outputs = machine.run(inputs)
            last_output = outputs.pop()
        if last_output > max_thruster:
            max_thruster = last_output

    return max_thruster

def feedback_loop(inputfile):
    max_thruster = 0
    code = IntcodeVM.read_intcode(inputfile)
    for phases in permutations([5,6,7,8,9]):
        done = False

        #Initialise machines
        machines = []
        for phase in phases:
            machine = IntcodeVM(code)
            machine.run([phase])
            machines.append(machine)

        last_output = 0
        while not done:
            for machine in machines:
                last_output = machine.resume([last_output])[-1]
                if not machine.waiting:
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
