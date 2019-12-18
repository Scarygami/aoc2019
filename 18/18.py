import os
import sys
from time import time

currentdir = os.path.dirname(os.path.abspath(__file__))

DIRECTIONS = [(1, 0), (-1, 0), (0, 1), (0, -1)]


def load_grid(filename):
    with open(filename, "r") as f:
        return [[c for c in line] for line in f.read().splitlines()]


def is_key(c):
    return c.isalpha() and c.islower()


def is_door(c):
    return c.isalpha() and c.isupper()


def find_next_keys(grid, position, keys):
    """BFS to find all the keys that can be reached in current state,
    and how many steps are necessary to get there"""
    frontiers = [(position, 0)]
    paths = {}
    visited = {
        position: 0
    }
    while len(frontiers) > 0:
        new_frontiers = []
        for frontier in frontiers:
            (x, y), steps = frontier
            steps = steps + 1
            for (dx, dy) in DIRECTIONS:
                nx = x + dx
                ny = y + dy
                if nx < 0 or nx >= len(grid[y]):
                    continue
                if ny < 0 or ny >= len(grid):
                    continue
                if grid[ny][nx] == "#":
                    continue
                if is_door(grid[ny][nx]) and grid[ny][nx].lower() not in keys:
                    # Can't continue through closed door
                    continue

                if (nx, ny) in visited and visited[(nx, ny)] <= steps:
                    # Been here before with fewer steps
                    continue
                visited[(nx, ny)] = steps

                if is_key(grid[ny][nx]) and grid[ny][nx] not in keys:
                    # Found a new key, stop here for now
                    paths[grid[ny][nx]] = ((nx, ny), steps)
                    continue

                # In all other cases we have to continue searching
                new_frontiers.append(((nx, ny), steps))

        frontiers = new_frontiers

    return paths


def shortest_path(filename):
    grid = load_grid(filename)
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            c = grid[y][x]
            if c == "@":
                start = (x, y)
                break
        else:
            continue
        break

    # BFS for all possible paths through maze
    # state = (position, keys): steps
    states = {
      (start, ""): 0
    }

    while True:
        new_states = {}
        for (position, keys), steps in states.items():
            paths = find_next_keys(grid, position, keys)
            for key, (new_position, new_steps) in paths.items():
                new_steps = steps + new_steps
                new_keys = list(keys)
                new_keys.append(key)
                new_keys.sort()
                new_keys = "".join(new_keys)
                if (new_position, new_keys) in new_states and new_states[(new_position, new_keys)] <= new_steps:
                    # Same state already reached in fewer steps > skip
                    # This significantly reduced the search space
                    continue
                new_states[(new_position, new_keys)] = new_steps

        if len(new_states) == 0:
            break

        states = new_states

    return min(states[state] for state in states)


def shortest_path2(filename):
    grid = load_grid(filename)

    starts = []
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            c = grid[y][x]
            if c == "@":
                grid[y-1][x-1] = "@"
                grid[y-1][x] = "#"
                grid[y-1][x+1] = "@"
                grid[y][x-1] = "#"
                grid[y][x] = "#"
                grid[y][x+1] = "#"
                grid[y+1][x-1] = "@"
                grid[y+1][x] = "#"
                grid[y+1][x+1] = "@"
                starts = [
                  (x-1, y-1),
                  (x-1, y+1),
                  (x+1, y-1),
                  (x+1, y+1)
                ]
                break
        else:
            continue
        break

    # BFS for all possible paths through maze
    # state = (positions, keys): steps
    states = {
      ((starts[0], starts[1], starts[2], starts[3]), frozenset()): 0
    }

    while True:
        new_states = {}
        for (positions, keys), steps in states.items():
            for p, position in enumerate(positions):
                paths = find_next_keys(grid, position, keys)
                for key, (new_position, new_steps) in paths.items():
                    new_steps = steps + new_steps
                    new_keys = set(keys)
                    new_keys.add(key)
                    new_keys = frozenset(new_keys)

                    new_positions = list(positions).copy()
                    new_positions[p] = new_position
                    new_positions = tuple(new_positions)

                    if (new_positions, new_keys) in new_states and new_states[(new_positions, new_keys)] <= new_steps:
                        # Exact same state already reached in fewer steps > skip
                        # This significantly reduced the search space
                        continue
                    new_states[(new_positions, new_keys)] = new_steps

        if len(new_states) == 0:
            break

        states = new_states

    return min(states[state] for state in states)


assert shortest_path(os.path.join(currentdir, "testinput1.txt")) == 8
assert shortest_path(os.path.join(currentdir, "testinput2.txt")) == 86
assert shortest_path(os.path.join(currentdir, "testinput3.txt")) == 132
assert shortest_path(os.path.join(currentdir, "testinput4.txt")) == 136
assert shortest_path(os.path.join(currentdir, "testinput5.txt")) == 81

start = time()
result = shortest_path(os.path.join(currentdir, "input.txt"))
end = time()
print("Part 1: %s (%.2f s)" % (result, end - start))

assert shortest_path2(os.path.join(currentdir, "testinput6.txt")) == 8
assert shortest_path2(os.path.join(currentdir, "testinput7.txt")) == 24
assert shortest_path2(os.path.join(currentdir, "testinput8.txt")) == 32
assert shortest_path2(os.path.join(currentdir, "testinput9.txt")) == 72

start = time()
result = shortest_path2(os.path.join(currentdir, "input.txt"))
end = time()
print("Part 2: %s (%.2f s)" % (result, end - start))
