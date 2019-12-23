import os
currentdir = os.path.dirname(os.path.abspath(__file__))


def calculate_fuel(mass):
    """Calculates the fuel necessary for the provided mass."""

    return (mass // 3) - 2


def calculate_total_fuel(mass):
    """Calculates the fuel necessary for the provided mass including fuel."""

    fuel = calculate_fuel(mass)
    if fuel < 0:
        return 0
    return fuel + calculate_total_fuel(fuel)


def total_fuel(inputfile, include_fuel=True):
    """Calculates the total fuel for the provided puzzle input file.

    Parameters
    ----------
    inputfile : str
        Name/path of file that contains the puzzle input

    include_fuel : bool
        Whether to include fuel in total fuel calculation
    """
    fuel = 0
    with open(inputfile, "r") as f:
        for line in f:
            mass = int(line)
            if include_fuel:
                fuel = fuel + calculate_total_fuel(mass)
            else:
                fuel = fuel + calculate_fuel(mass)

    return fuel


assert calculate_fuel(12) == 2
assert calculate_fuel(14) == 2
assert calculate_fuel(1969) == 654
assert calculate_fuel(100756) == 33583
assert total_fuel(os.path.join(currentdir, "testinput.txt"), False) == 34241
assert total_fuel(os.path.join(currentdir, "testinput.txt"), True) == 51316
assert calculate_total_fuel(14) == 2
assert calculate_total_fuel(1969) == 966
assert calculate_total_fuel(100756) == 50346

print("Part 1: %s" % (total_fuel(os.path.join(currentdir, "input.txt"), False)))
print("Part 2: %s" % (total_fuel(os.path.join(currentdir, "input.txt"), True)))
