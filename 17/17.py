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

try:
    from asciimatics.screen import Screen
except ImportError:
    print("Couldn't find asciimatics package, please install with `pip install asciimatics`")
    exit(1)


def create_grid(inputfile):
    source = IntcodeVM.read_intcode(inputfile)
    machine = IntcodeVM(source, silent=True)
    outputs = machine.run()
    grid = []
    line = []

    for output in outputs:
        if output == 10:
            if len(line) > 0:
                grid.append(line)
            line = []
        else:
            line.append(chr(output))

    return grid


def total_alignment(grid):
    total = 0
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[y]) - 1):
            if grid[y][x - 1:x + 2] != ["#", "#", "#"]:
                continue
            if grid[y - 1][x] != "#":
                continue
            if grid[y + 1][x] != "#":
                continue

            total = total + x * y

    return total


def is_on_scaffold(grid, x, y):
    if y >= 0 and y < len(grid):
        if x >= 0 and x < len(grid[y]):
            if grid[y][x] == "#":
                return True

    return False


def find_path(grid):
    # find position of robot
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == "^":
                position = (y, x)
                direction = (-1, 0)
            if grid[y][x] == "v":
                position = (y, x)
                direction = (1, 0)
            if grid[y][x] == "<":
                position = (y, x)
                direction = (0, -1)
            if grid[y][x] == ">":
                position = (y, x)
                direction = (0, 1)

    TURNS = {  # direction: [L, R]
      (-1, 0): [(0, -1), (0, 1)],
      (1, 0): [(0, 1), (0, -1)],
      (0, -1): [(1, 0), (-1, 0)],
      (0, 1): [(-1, 0), (1, 0)]
    }

    moves = []
    steps = 0
    while True:
        y, x = position
        dy, dx = direction
        if is_on_scaffold(grid, x + dx, y + dy):
            # robot can continue in this direction
            position = (y + dy, x + dx)
            steps = steps + 1
            continue

        if steps > 0:
            moves.append(str(steps))

        no_more_moves = True
        for lr in range(2):
            dy, dx = TURNS[direction][lr]
            if is_on_scaffold(grid, x + dx, y + dy):
                direction = (dy, dx)
                no_more_moves = False
                steps = 0
                if lr == 0:
                    moves.append("L")
                else:
                    moves.append("R")
                break

        if no_more_moves:
            break

    return ",".join(moves)


class GridDrawer(object):
    def __init__(self, screen):
        self.x = 1
        self.y = 1
        self.screen = screen

    def add_output(self, output):
        if output > 255:
            # Non ascii-character
            return

        if output == 10:
            if self.x == 1:
                # Last line reached
                self.screen.move(0, 0)
                self.screen.print_at(" ", 0, 0)
                self.screen.refresh()
                self.x = 1
                self.y = 1
            else:
                self.y = self.y + 1
                self.x = 1
        else:
            # Flipped output for better dimensions in terminal window
            output = chr(output)
            if output == "^":
                output = "<"
            elif output == ">":
                output = "v"
            elif output == "v":
                output = ">"
            elif output == "<":
                output = "^"
            elif output == ".":
                output = " "

            self.screen.print_at(output, self.y, self.x)
            self.x = self.x + 1


def move_robot(inputfile, moves, screen):
    source = IntcodeVM.read_intcode(inputfile)
    drawer = GridDrawer(screen)
    source[0] = 2
    machine = IntcodeVM(source, silent=True, output_func=drawer.add_output)
    outputs = machine.run(moves)
    sleep(2)
    return outputs.pop()


def day_17(screen):
    grid = create_grid(os.path.join(currentdir, "input.txt"))
    print("Part 1: %s" % total_alignment(grid))

    print("Move sequence: %s" % find_path(grid))

    """
    I've split up the movement instructions manually, after finding the full path,
    which was definitely quicker than finding an algorithm to do so for me:

    A = L,12,L,12,R,12
    B = L,8,L,8,R,12,L,8,L,8
    C = L,10,R,8,R,12

    A,A,B,C,C,A,B,C,A,B
    """
    input_str = "A,A,B,C,C,A,B,C,A,B\nL,12,L,12,R,12\nL,8,L,8,R,12,L,8,L,8\nL,10,R,8,R,12\ny\n"
    print("Part 2: %s" % move_robot(os.path.join(currentdir, "input.txt"), input_str, screen))


Screen.wrapper(day_17)
