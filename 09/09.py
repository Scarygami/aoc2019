import os
import sys
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from lib import intcode

testcode = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
result = intcode.run_intcode([109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]).outputs
for i in range(len(testcode)):
    assert testcode[i] == result[i]

result = intcode.run_intcode([104,1125899906842624,99]).outputs
assert result.pop() == 1125899906842624

outputs = intcode.run_intcode(intcode.read_intcode(os.path.join(currentdir, "input.txt")), [1]).outputs
print("Part 1: %s" % outputs.pop())

outputs = intcode.run_intcode(intcode.read_intcode(os.path.join(currentdir, "input.txt")), [2]).outputs
print("Part 2: %s" % outputs.pop())
