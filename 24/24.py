import os
currentdir = os.path.dirname(os.path.abspath(__file__))

SIZE = 5
CENTER = 0
EDGE = 1

NEIGHBOURS = {
    (-1, 0): ((1, 2), ((4, 0), (4, 1), (4, 2), (4, 3), (4, 4))),
    (1, 0): ((3, 2), ((0, 0), (0, 1), (0, 2), (0, 3), (0, 4))),
    (0, -1): ((2, 1), ((0, 4), (1, 4), (2, 4), (3, 4), (4, 4))),
    (0, 1): ((2, 3), ((0, 0), (1, 0), (2, 0), (3, 0), (4, 0)))
}

EDGES = set(sum([list(value[EDGE]) for value in NEIGHBOURS.values()], []))
CENTERS = [value[CENTER] for value in NEIGHBOURS.values()]


def read_input(inputfile):
    with open(inputfile, "r") as f:
        return [[c for c in line] for line in f.read().splitlines()]


def count_neighbours(generation, x, y):
    count = 0
    for dx, dy in NEIGHBOURS:
        nx = x + dx
        ny = y + dy
        if nx >= 0 and nx < SIZE and ny >= 0 and ny < SIZE:
            if generation[ny][nx] == "#":
                count = count + 1

    return count


def evolve(generation):
    new_generation = []
    for y in range(SIZE):
        line = []
        for x in range(SIZE):
            neighbours = count_neighbours(generation, x, y)
            if generation[y][x] == "#":
                if neighbours == 1:
                    line.append("#")
                else:
                    line.append(".")
            else:
                if neighbours == 1 or neighbours == 2:
                    line.append("#")
                else:
                    line.append(".")

        new_generation.append(line)

    return new_generation


def biodiversity(generation):
    value = 0
    for y in range(SIZE):
        for x in range(SIZE):
            if generation[y][x] == "#":
                value = value + 2 ** (y * SIZE + x)
    return value


def generation_key(generation):
    return "".join("".join(line) for line in generation)


def count_neighbours_multi(generation, x, y, parent):
    count = 0
    for dx, dy in NEIGHBOURS:
        nx = x + dx
        ny = y + dy
        if nx >= 0 and nx < SIZE and ny >= 0 and ny < SIZE:
            cell = generation[ny][nx]
            if cell == "#":
                count = count + 1
            elif isinstance(cell, list):
                for ex, ey in NEIGHBOURS[(dx, dy)][EDGE]:
                    if cell[ey][ex] == "#":
                        count = count + 1
        elif parent:
            px, py = NEIGHBOURS[(dx, dy)][CENTER]
            if parent[py][px] == "#":
                count = count + 1

    return count


def multi_evolve(generation, parent=None):

    # Determine if we need to go one level deeper
    if generation[2][2] is None:
        bugs_in_center = False
        for x, y in CENTERS:
            if generation[y][x] == "#":
                bugs_in_center = True
                break

        if bugs_in_center:
            generation[2][2] = [
                [".", ".", ".", ".", "."],
                [".", ".", ".", ".", "."],
                [".", ".", None, ".", "."],
                [".", ".", ".", ".", "."],
                [".", ".", ".", ".", "."]
            ]

    # Determine if we need to go one level higher
    if parent is None:
        bugs_on_edge = False

        for x, y in EDGES:
            if generation[y][x] == "#":
                bugs_on_edge = True
                break

        if bugs_on_edge:
            generation = [
                [".", ".", ".", ".", "."],
                [".", ".", ".", ".", "."],
                [".", ".", generation, ".", "."],
                [".", ".", ".", ".", "."],
                [".", ".", ".", ".", "."]
            ]

    new_generation = []
    for y in range(SIZE):
        line = []
        for x in range(SIZE):
            neighbours = count_neighbours_multi(generation, x, y, parent)
            cell = generation[y][x]
            if cell == "#":
                if neighbours == 1:
                    line.append("#")
                else:
                    line.append(".")
            elif cell == ".":
                if neighbours == 1 or neighbours == 2:
                    line.append("#")
                else:
                    line.append(".")
            elif isinstance(cell, list):
                line.append(multi_evolve(cell, generation))
            else:
                line.append(None)

        new_generation.append(line)

    return new_generation


def count_bugs(generation):
    count = 0
    for line in generation:
        for cell in line:
            if cell == "#":
                count = count + 1
            elif isinstance(cell, list):
                count = count + count_bugs(cell)

    return count


def part1(inputfile):
    generation = read_input(inputfile)
    generations = []
    while generation_key(generation) not in generations:
        generations.append(generation_key(generation))
        generation = evolve(generation)

    return biodiversity(generation)


def part2(inputfile, minutes=200):
    generation = read_input(inputfile)
    generation[2][2] = None

    for _ in range(minutes):
        generation = multi_evolve(generation)

    return count_bugs(generation)


assert generation_key(evolve(["....#", "#..#.", "#..##", "..#..", "#...."])) == "#..#.####.###.###.##.##.."
assert generation_key(evolve(["#..#.", "####.", "###.#", "##.##", ".##.."])) == "#####....#....#...#.#.###"
assert generation_key(evolve(["#####", "....#", "....#", "...#.", "#.###"])) == "#....####....###.##..##.#"
assert generation_key(evolve(["#....", "####.", "...##", "#.##.", ".##.#"])) == "####.....###..#.....##..."

assert biodiversity([".....", ".....", ".....", "#....", ".#..."]) == 2129920

assert part1(os.path.join(currentdir, "testinput1.txt")) == 2129920
assert part2(os.path.join(currentdir, "testinput1.txt"), 10) == 99

print("Part 1: %s" % part1(os.path.join(currentdir, "input.txt")))
print("Part 2: %s" % part2(os.path.join(currentdir, "input.txt")))
