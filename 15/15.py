import os
import sys
from time import sleep

currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

try:
    from lib.intcode import IntcodeVM
except ImportError:
    print("Intcode library could not be found")
    exit(1)

WALL = 0
FREE = 1
OS = 2

DIRECTIONS = [(0, -1), (0, 1), (-1, 0), (1, 0)]

# Initiliase droid
machine = IntcodeVM(IntcodeVM.read_intcode(os.path.join(currentdir, "input.txt")), False, True)
machine.run()

os_pos = None

# Breadth-first search
frontiers = [
    # machine / position / steps
    (machine, (0, 0), 0)
]
distances = {
    (0, 0): 0
}
areamap = {
    (0, 0): FREE
}
while len(frontiers) > 0:
    machine, position, steps = frontiers.pop(0)
    for m in range(len(DIRECTIONS)):
        new_machine = machine.copy()
        outputs = new_machine.resume([m + 1])
        dx, dy = DIRECTIONS[m]
        new_position = (position[0] + dx, position[1] + dy)
        new_steps = steps + 1
        areamap[new_position] = outputs[0]

        if outputs[0] == WALL:
            continue

        if new_position in distances and new_steps >= distances[new_position]:
            # this position was already reached in fewer steps before
            continue

        distances[new_position] = new_steps

        if outputs[0] == OS:
            os_pos = new_position

        frontiers.append((new_machine, new_position, new_steps))


print("Part 1: %s" % distances[os_pos])

# Slightly different breadth-first search
frontiers = [os_pos]
minutes = 0
while len(frontiers) > 0:
    new_frontiers = []
    for frontier in frontiers:
        for (dx, dy) in DIRECTIONS:
            new_frontier = (frontier[0] + dx, frontier[1] + dy)
            if areamap.get(new_frontier, WALL) == FREE:
                areamap[new_frontier] = OS
                new_frontiers.append(new_frontier)

    frontiers = new_frontiers
    if len(frontiers) > 0:
        minutes = minutes + 1

print("Part 2: %s" % minutes)
