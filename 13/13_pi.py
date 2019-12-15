#!/usr/bin/python3

import os
import sys
import RPi.GPIO as GPIO
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

GPIO.setmode(GPIO.BCM)

GPIO.setup(14, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(15, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def pi_input():
    while True:
        left = GPIO.input(14)
        middle = GPIO.input(15)
        right = GPIO.input(18)

        if left == False:
            return -1
        if middle == False:
            return 0
        if right == False:
            return 1
           

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
            5, max_y
        )
        screen.print_at(
            "Score: %s" % score,
            5, max_y + 1
        )
        screen.move(0, 0)
        screen.refresh()
        sleep(0.2)

        move = pi_input()


    screen.print_at(
        "Game over!",
        5, max_y // 2
    )
    screen.refresh()
    sleep(2)


def game(screen):
    play_game(os.path.join(currentdir, "input.txt"), screen)


Screen.wrapper(game)
