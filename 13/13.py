import os
import sys
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from lib.intcode import IntcodeVM

SYMBOLS = [" ", "#", "X", "_", "o"]


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


def print_grid(grid):
    minx, miny = min(grid.keys())
    maxx, maxy = max(grid.keys())

    clear()
    for y in range(miny, maxy + 1):
        line = ""
        for x in range(minx, maxx + 1):
            line = line + SYMBOLS[grid[(x, y)]]
        print(line)


def play_game(inputfile):
    source = IntcodeVM.read_intcode(inputfile)
    source[0] = 2
    machine = IntcodeVM(source, silent=True)
    outputs = machine.run()
    grid = {}
    score = 0
    total_bricks = 0
    while machine.waiting:
        for o in range(0, len(outputs), 3):
            x, y, tile = outputs[o:o+3]
            if x == -1 and y == 0:
                score = tile
            else:
                grid[(x, y)] = tile

        if total_bricks == 0:
            total_bricks = sum(1 for pos in grid if grid[pos] == 2)

        print_grid(grid)
        print("Bricks left: %s / %s" % (sum(1 for pos in grid if grid[pos] == 2), total_bricks))
        print("Score: %s" % score)

        # Breakout AI!!
        paddle = [key for key in grid if grid[key] == 3][0]
        ball = [key for key in grid if grid[key] == 4][0]
        if paddle[0] < ball[0]:
            value = 1
        elif paddle[0] > ball[0]:
            value = -1
        else:
            value = 0

        outputs = machine.resume([value])

    for o in range(0, len(outputs), 3):
        x, y, tile = outputs[o:o+3]
        if x == -1 and y == 0:
            score = tile
        else:
            grid[(x, y)] = tile

    print_grid(grid)
    print("Score: %s" % score)


play_game(os.path.join(currentdir, "input.txt"))
