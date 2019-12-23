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


class Network(object):

    def __init__(self, source, computers=50):
        self.computers = []
        self.packets = []
        self.outputs = []
        self.idle = []
        self.nat_package = None
        self.last_nat_package = None

        for c in range(computers):
            computer = IntcodeVM(source, silent=True)
            self.idle.append(0)
            self.packets.append([])
            output = computer.run([c])
            self.outputs.append(output)
            computer.stepwise = True
            self.computers.append(computer)

    def run(self, nat=False):
        while True:
            self.handle_outputs()

            if nat:
                if sum(1 for i in self.idle if i > 10) == len(self.computers) and self.nat_package:
                    # all machines have been idle for a while
                    self.packets[0].append(self.nat_package)
                    self.idle[0] = 0
                    if self.last_nat_package and self.last_nat_package[1] == self.nat_package[1]:
                        return self.nat_package[1]

                    self.last_nat_package = self.nat_package.copy()
            else:
                if self.nat_package:
                    return self.nat_package[1]

            for c, computer in enumerate(self.computers):
                if computer.waiting:
                    if len(self.packets[c]) > 0:
                        packet = self.packets[c].pop(0)
                        output = computer.resume(packet)
                        self.idle[c] = 0
                    else:
                        output = computer.resume([-1])
                        self.idle[c] = self.idle[c] + 1
                else:
                    output = computer.resume()

                if len(output) > 0:
                    self.idle[c] = 0
                    self.outputs[c].extend(output)

    def handle_outputs(self):
        for c in range(len(self.computers)):
            if len(self.outputs[c]) < 3:
                continue

            end = (len(self.outputs[c]) // 3) * 3

            for o in range(0, end, 3):
                dest = self.outputs[c][o]
                x = self.outputs[c][o + 1]
                y = self.outputs[c][o + 2]
                if dest == 255:
                    self.nat_package = [x, y]
                else:
                    self.packets[dest].append([x, y])

            self.outputs[c] = self.outputs[c][end:]


source = IntcodeVM.read_intcode(os.path.join(currentdir, "input.txt"))
network = Network(source)
print("Part 1: %s" % network.run())
print("Part 2: %s" % network.run(True))
