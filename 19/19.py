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


def check_square(machine, startx, starty, size=100):
    if not check_row(machine, startx, starty, size):
        return False
    if not check_row(machine, startx, starty + size - 1, size):
        return False
    return True


def check_row(machine, startx, y, size=100):
    if not check_field(machine, startx, y):
        return False
    if not check_field(machine, startx + size - 1, y):
        return False
    return True


def check_field(machine, x, y):
    if machine.run([x, y]) == [1]:
        return True
    return False


def find_square(machine, size=100):
    y = -1
    minx = 0
    while True:
        y = y + 1
        startx = None
        for x in range(minx, minx + 5):
            if check_field(machine, x, y):
                startx = x
                minx = x
                break

        if startx is None:
            # No tractor beam in this row
            continue

        x = startx
        while check_row(machine, x, y, size):
            if check_square(machine, x, y, size):
                return (x, y)
            x = x + 1


machine = IntcodeVM(IntcodeVM.read_intcode(os.path.join(currentdir, "input.txt")), silent=True)
affected = []
for y in range(50):
    for x in range(50):
        if check_field(machine, x, y):
            affected.append((x, y))

print("Part 1: %s" % len(affected))


x, y = find_square(machine, 100)
print("Part 2: %s" % (x * 10000 + y))
