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
            if grid[y][x] in "^v<>":
                position = (y, x)
                if grid[y][x] == "^":
                    direction = (-1, 0)
                elif grid[y][x] == "v":
                    direction = (1, 0)
                elif grid[y][x] == "<":
                    direction = (0, -1)
                elif grid[y][x] == ">":
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
        self.visited = []

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
            if output in "^":
                output = "<"
            elif output == ">":
                output = "v"
            elif output == "v":
                output = ">"
            elif output == "<":
                output = "^"
            elif output == ".":
                output = " "
            elif output == "#":
                if (self.x, self.y) in self.visited:
                    output = "█"
                else:
                    output = "░"

            if output in "^<>v":
                self.visited.append((self.x, self.y))

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


def replace_sequence(sequence, part, letter):
    length = len(part)
    p = 0
    new_sequence = []
    while p < len(sequence):
        if sequence[p:p+length] == part:
            new_sequence.append(letter)
            p = p + length
        else:
            new_sequence.append(sequence[p])
            p = p + 1
    return new_sequence


def compress(sequence, left_parts="ABC"):
    if isinstance(sequence, str):
        sequence = sequence.split(",")

    letter = left_parts[0]
    left_parts = left_parts[1:]

    start = 0
    while sequence[start] in "ABC":
        # Find the first position that hasn't been compressed yet
        start = start + 1

    for l in range(start, len(sequence)):
        if sequence[l] in "ABC":
            # reached a pre-compressed area
            break

        part = sequence[start:(l+1)]
        part_str = ",".join(part)
        if len(part_str) > 20:
            # sequence has gotten too long
            break

        new_sequence = replace_sequence(sequence, part, letter)
        if len(left_parts) > 0:
            new_sequence_str, parts = compress(new_sequence, left_parts)
            if not new_sequence_str:
                continue
            parts.insert(0, part_str)
            return (new_sequence_str, parts)
        else:
            new_sequence_str = ",".join(new_sequence)
            if len(new_sequence_str) > 20:
                continue
            return (new_sequence_str, [part_str])

    # No solution found...
    return (None, None)


def day_17(screen):
    grid = create_grid(os.path.join(currentdir, "input.txt"))
    print("Part 1: %s" % total_alignment(grid))

    sequence = find_path(grid)
    main_sequence, parts = compress(sequence)
    input_str = main_sequence + "\n" + "\n".join(parts) + "\ny\n"
    print("Part 2: %s" % move_robot(os.path.join(currentdir, "input.txt"), input_str, screen))


Screen.wrapper(day_17)
