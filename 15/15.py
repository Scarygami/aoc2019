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

WALL = 0
FREE = 1
OS = 2
DROID = 3

COLORS = [7, 0, 4, 3]

NORTH = 1
SOUTH = 2
WEST = 3
EAST = 4

MOVES = [NORTH, SOUTH, WEST, EAST]

DIRECTIONS = {
    NORTH: (0, -1),
    SOUTH: (0, 1),
    WEST: (-1, 0),
    EAST: (1, 0)
}

REVERSE = {
    NORTH: SOUTH,
    SOUTH: NORTH,
    WEST: EAST,
    EAST: WEST
}


def draw_map(area_map, droid_position, screen, dimensions):
    if not screen:
        return

    minx, miny, maxx, maxy = dimensions
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            screen.print_at("██", (x - minx) * 2, y - miny, COLORS[area_map.get((x, y), WALL)])

    if droid_position:
        x, y = droid_position
        screen.print_at("██", (x - minx) * 2, y - miny, COLORS[DROID])

    screen.refresh()


def explore(droid, position=(0, 0), area_map=None, distance_map=None, steps=0, screen=None, dimensions=None):
    """It felt unfair to use BFS for the first part,
    since it explicitely stated that we have only one droid,
    so here is one droid exploring the whole area on its own."""

    if area_map is None:
        area_map = {(0, 0): FREE}
    if distance_map is None:
        distance_map = {(0, 0): 0}

    x, y = position
    steps = steps + 1
    draw_map(area_map, position, screen, dimensions)

    for move in MOVES:
        dx, dy = DIRECTIONS[move]
        new_position = (x + dx, y + dy)

        if new_position in distance_map and distance_map[new_position] <= steps:
            continue

        distance_map[new_position] = steps
        output = droid.resume([move])[0]
        area_map[new_position] = output
        if output == 0:
            continue

        # Continue along the new path
        explore(droid, new_position, area_map, distance_map, steps, screen, dimensions)

        # backtracking
        droid.resume([REVERSE[move]])
        draw_map(area_map, position, screen, dimensions)

    return (area_map, distance_map)


def maze(screen):
    # Initiliase droid
    droid = IntcodeVM(IntcodeVM.read_intcode(os.path.join(currentdir, "input.txt")), False, True)

    # One run to determine the dimensions of the grid
    droid.run()
    area_map, _ = explore(droid)
    minx = min(pos[0] for pos in area_map)
    maxx = max(pos[0] for pos in area_map)
    miny = min(pos[1] for pos in area_map)
    maxy = max(pos[1] for pos in area_map)
    dimensions = (minx, miny, maxx, maxy)

    # Actual run with visualization
    droid.run()
    area_map, distance_map = explore(droid, screen=screen, dimensions=dimensions)
    os_pos = [pos for pos in area_map if area_map[pos] == OS][0]

    # breadth-first algorithm for spreading the oxygen
    frontiers = [os_pos]
    minutes = 0
    while len(frontiers) > 0:
        new_frontiers = []
        for frontier in frontiers:
            for (dx, dy) in DIRECTIONS.values():
                new_frontier = (frontier[0] + dx, frontier[1] + dy)
                if area_map.get(new_frontier, WALL) == FREE:
                    area_map[new_frontier] = OS
                    draw_map(area_map, None, screen, dimensions)
                    new_frontiers.append(new_frontier)

        frontiers = new_frontiers
        if len(frontiers) > 0:
            minutes = minutes + 1

    input()
    print("Part 1: %s" % distance_map[os_pos])
    print("Part 2: %s" % minutes)


Screen.wrapper(maze)
