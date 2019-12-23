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


def handle_outputs(packets, outputs, n):
    if len(outputs[n]) < 3:
        return

    end = (len(outputs[n]) // 3) * 3

    for o in range(0, end, 3):
        dest = outputs[n][o]
        x = outputs[n][o + 1]
        y = outputs[n][o + 2]
        packets[dest].append([x, y])

    outputs[n] = outputs[n][end:]


def initialise_network(source):
    machines = {}
    packets = {}
    outputs = {}
    idle = {}
    packets[255] = []

    for n in range(50):
        machine = IntcodeVM(source, silent=True)
        idle[n] = 0
        packets[n] = []
        outputs[n] = []
        outputs[n].extend(machine.run([n]))
        handle_outputs(packets, outputs, n)

        machine.stepwise = True
        machines[n] = machine

    return machines, packets, outputs, idle


def run_network(source, nat=False):
    machines, packets, outputs, idle = initialise_network(source)
    last_nat_value = None

    while True:
        if nat:
            if len([1 for state in idle if idle[state] > 500]) == 50:
                # all machines have been idle for a while
                nat_value = packets[255][-1]
                packets[0].append(nat_value)
                idle[0] = 0
                if last_nat_value and last_nat_value == nat_value[1]:
                    print("Part 2: %s" % nat_value[1])
                    break
                last_nat_value = nat_value[1]

        for n in range(50):
            machine = machines[n]
            if machine.waiting:
                if len(packets[n]) > 0:
                    packet = packets[n].pop(0)
                    output = machine.resume(packet)
                else:
                    output = machine.resume([-1])
                    idle[n] = idle[n] + 1
            else:
                output = machine.resume()

            if len(output) > 0:
                idle[n] = 0
                outputs[n].extend(output)
                handle_outputs(packets, outputs, n)
                if not nat and len(packets[255]) > 0:
                    print("Part 1: %s" % packets[255][0][1])
                    break
        else:
            continue
        break


source = IntcodeVM.read_intcode(os.path.join(currentdir, "input.txt"))
run_network(source, False)
run_network(source, True)
