import os
import sys
from time import time

currentdir = os.path.dirname(os.path.abspath(__file__))

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def load_grid(filename):
    with open(filename, "r") as f:
        grid = [[c for c in line] for line in f.read().splitlines()]

    # Remove all dead ends
    while True:
        removed = 0
        for y in range(3, len(grid) - 3):
            for x in range(3, len(grid[y]) - 3):
                if grid[y][x] == ".":
                    neighbours = [grid[y + dy][x + dx] for (dx, dy) in DIRECTIONS]
                    if neighbours.count("#") == 3:
                        grid[y][x] = "#"
                        removed = removed + 1

        if removed == 0:
            break

    # Find start, end and portals
    tmp_portals = {}
    for y in range(1, len(grid) - 1):
        for x in range(1, len(grid[y]) - 1):
            if grid[y][x].isalpha():
                portal_key = None
                # Portal on top
                if grid[y-1][x].isalpha() and grid[y+1][x] == ".":
                    portal_key = grid[y-1][x] + grid[y][x]

                # Portal on bottom
                if grid[y+1][x].isalpha() and grid[y-1][x] == ".":
                    portal_key = grid[y][x] + grid[y+1][x]

                # Portal on left
                if grid[y][x-1].isalpha() and grid[y][x+1] == ".":
                    portal_key = grid[y][x-1] + grid[y][x]

                # Portal on right
                if grid[y][x+1].isalpha() and grid[y][x-1] == ".":
                    portal_key = grid[y][x] + grid[y][x+1]

                if portal_key:
                    portal = tmp_portals.get(portal_key, [])
                    portal.append((x, y))
                    tmp_portals[portal_key] = portal

    x, y = tmp_portals["AA"][0]
    for dx, dy in DIRECTIONS:
        if grid[y + dy][x + dx] == ".":
            start = (x + dx, y + dy)
            break
    del tmp_portals["AA"]

    x, y = tmp_portals["ZZ"][0]
    for dx, dy in DIRECTIONS:
        if grid[y + dy][x + dx] == ".":
            end = (x + dx, y + dy)
            break
    del tmp_portals["ZZ"]

    portals = {}
    for portal in tmp_portals.values():
        if len(portal) == 2:
            for p in range(2):
                source = portal[p]
                x, y = portal[1 - p]
                for dx, dy in DIRECTIONS:
                    if grid[y + dy][x + dx] == ".":
                        target = (x + dx, y + dy)
                        break
                portals[source] = target

    return grid, portals, start, end


def shortest_path(filename):
    grid, portals, start, end = load_grid(filename)

    visited = {start: 0}

    frontiers = [
        (start, 0)
    ]

    while len(frontiers) > 0:
        new_frontiers = []
        for (x, y), steps in frontiers:
            steps = steps + 1
            for dx, dy in DIRECTIONS:
                nx = x + dx
                ny = y + dy
                if grid[ny][nx] == "#":
                    continue
                nx, ny = portals.get((nx, ny), (nx, ny))
                if (nx, ny) in visited:
                    if visited[(nx, ny)] <= steps:
                        continue
                visited[(nx, ny)] = steps
                if (nx, ny) == end:
                    return steps

                if grid[ny][nx] == ".":
                    new_frontiers.append(((nx, ny), steps))

        frontiers = new_frontiers


def is_outside_portal(grid, x, y):
    if x <= 1:
        return True
    if y <= 1:
        return True
    if x >= len(grid[y]) - 2:
        return True
    if y >= len(grid) - 2:
        return True
    return False


def shortest_path2(filename):
    grid, portals, start, end = load_grid(filename)

    visited = {(start, 0): 0}

    frontiers = [
        (start, 0, 0)
    ]

    while len(frontiers) > 0:
        new_frontiers = []
        for (x, y), level, steps in frontiers:
            steps = steps + 1
            for dx, dy in DIRECTIONS:
                nx = x + dx
                ny = y + dy
                nl = level
                if grid[ny][nx] == "#":
                    continue

                if (nx, ny) in portals:
                    if is_outside_portal(grid, nx, ny):
                        if nl == 0:
                            continue
                        nl = nl - 1
                    else:
                        nl = nl + 1

                    nx, ny = portals[(nx, ny)]

                if ((nx, ny), nl) in visited:
                    if visited[((nx, ny), nl)] <= steps:
                        continue
                visited[((nx, ny), nl)] = steps
                if (nx, ny) == end and nl == 0:
                    return steps

                if grid[ny][nx] == ".":
                    new_frontiers.append(((nx, ny), nl, steps))

        frontiers = new_frontiers


assert shortest_path(os.path.join(currentdir, "testinput1.txt")) == 23
assert shortest_path(os.path.join(currentdir, "testinput2.txt")) == 58

start = time()
result = shortest_path(os.path.join(currentdir, "input.txt"))
end = time()
print("Part 1: %s (%.2f s)" % (result, end - start))

assert shortest_path2(os.path.join(currentdir, "testinput1.txt")) == 26
assert shortest_path2(os.path.join(currentdir, "testinput3.txt")) == 396

start = time()
result = shortest_path2(os.path.join(currentdir, "input.txt"))
end = time()
print("Part 2: %s (%.2f s)" % (result, end - start))
