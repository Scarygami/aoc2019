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


EMPTY = 0
WALL = 1
BLOCK = 2
PADDLE = 3
BALL = 4
SYMBOLS = ["   ", "███", "███", "███", " ⬤ "]
COLORS = [0, 7, 3, 4, 2]


def play_game(inputfile, screen):
    source = IntcodeVM.read_intcode(inputfile)

    # Insert coin...
    source[0] = 2

    # Boot up arcade machine
    machine = IntcodeVM(source, silent=True)
    grid = {}
    score = 0
    total_bricks = 0
    max_y = 0
    move = None

    # Game loop
    while machine.waiting:
        if move is None:
            outputs = machine.run()
        else:
            outputs = machine.resume([move])

        for o in range(0, len(outputs), 3):
            x, y, tile = outputs[o:o+3]
            if x == -1 and y == 0:
                score = tile
            else:
                screen.print_at(SYMBOLS[tile], x * 3, y, COLORS[tile])
                grid[(x, y)] = tile

        if total_bricks == 0:
            total_bricks = sum(1 for pos in grid if grid[pos] == BLOCK)

        if max_y == 0:
            max_y = max(grid.keys())[1]

        screen.print_at(
            "Blocks left: %s / %s     " % (sum(1 for pos in grid if grid[pos] == 2), total_bricks),
            5, max_y + 1
        )
        screen.print_at(
            "Score: %s" % score,
            5, max_y + 2
        )
        screen.move(0, 0)
        screen.refresh()
        sleep(0.01)

        # Breakout AI!!
        paddle = [key for key in grid if grid[key] == PADDLE][0]
        ball = [key for key in grid if grid[key] == BALL][0]
        if paddle[0] < ball[0]:
            move = 1
        elif paddle[0] > ball[0]:
            move = -1
        else:
            move = 0

    screen.print_at(
        "All done, press ENTER to exit!",
        5, max_y // 2
    )
    screen.refresh()
    input()


def game(screen):
    play_game(os.path.join(currentdir, "input.txt"), screen)


Screen.wrapper(game)
