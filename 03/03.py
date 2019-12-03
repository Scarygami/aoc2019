import os
currentdir = os.path.dirname(os.path.abspath(__file__))

directions = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, -1),
    "D": (0, 1)
}

def draw_line(grid, number, instructions):
    """Draws one line into the grid. Returns intersections that occured

    Parameters
    ----------
    grid : dict
        grid to be filled

    number: int
        number of the line

    instructions: str
        line of instructions to draw the line directly from input file
    """

    intersections = []
    x = 0
    y = 0
    counter = 0
    for instruction in instructions.split(","):
        direction = directions[instruction[0]]
        steps = int(instruction[1:])
        for _ in range(steps):
            x = x + direction[0]
            y = y + direction[1]
            counter = counter + 1
            cell = grid.get((x,y), {})
            if number in cell:
                # Been here already before
                pass
            else:
                if len(cell) > 0:
                    intersections.append((x, y))
                cell[number] = counter
                grid[(x, y)] = cell

    return intersections

def create_grid(inputfile):
    """Creates the grid based on instruction in input file.
    Returns the grid as dict and a list of intersections.

    inputfile : str
        name/path of puzzle input file
    """

    grid = {}
    intersections = []
    row = 0
    with open(inputfile, "r") as f:
        for line in f:
            row = row + 1
            new_intersections = draw_line(grid, row, line)
            intersections.extend(new_intersections)

    return (grid, intersections)

def manhattan_distance(_, cell):
    return abs(cell[0]) + abs(cell[1])

def steps_distance(grid, cell):
    return sum(grid[cell].values())

def closest_intersection(inputfile, distance_function):
    """Returns the distance to closest intersection

    inputfile : str
        name/path of puzzle input file

    distance_function : function
        Function to calculate the distance
        Will get the grid and one cell-coordinate as parameters
    """

    grid, intersections = create_grid(inputfile)
    if len(intersections) == 0:
        return 0
    intersection = min(intersections, key=lambda i: distance_function(grid, i))
    return distance_function(grid, intersection)

assert closest_intersection(os.path.join(currentdir, "testinput1.txt"), manhattan_distance) == 6
assert closest_intersection(os.path.join(currentdir, "testinput2.txt"), manhattan_distance) == 159
assert closest_intersection(os.path.join(currentdir, "testinput3.txt"), manhattan_distance) == 135

print("Part 1: %s" % (closest_intersection(os.path.join(currentdir, "input.txt"), manhattan_distance)))

assert closest_intersection(os.path.join(currentdir, "testinput1.txt"), steps_distance) == 30
assert closest_intersection(os.path.join(currentdir, "testinput2.txt"), steps_distance) == 610
assert closest_intersection(os.path.join(currentdir, "testinput3.txt"), steps_distance) == 410

print("Part 2: %s" % (closest_intersection(os.path.join(currentdir, "input.txt"), steps_distance)))
