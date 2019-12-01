def calculate_fuel(mass):
    """Calculates the fuel necessary for the provided mass."""

    return (mass // 3) - 2

assert calculate_fuel(12) == 2
assert calculate_fuel(14) == 2
assert calculate_fuel(1969) == 654
assert calculate_fuel(100756) == 33583

def calculate_total_fuel(mass):
    """Calculates the fuel necessary for the provided mass including fuel."""

    fuel = calculate_fuel(mass)
    if fuel < 0:
        return 0
    return fuel + calculate_total_fuel(fuel)

assert calculate_total_fuel(14) == 2
assert calculate_total_fuel(1969) == 966
assert calculate_total_fuel(100756) == 50346

def total_fuel(inputfile, part1=True):
    """Calculates the total fuel for the provided puzzle input file.

    Parameters
    ----------
    inputfile : str
        Name/path of file that contains the puzzle input

    part1 : bool
        Whether to calculate according to part 1 or part 2 of the puzzle
    """
    fuel = 0
    with open(inputfile, "r") as f:
        for line in f:
            mass = int(line)
            if part1:
                fuel = fuel + calculate_fuel(mass)
            else:
                fuel = fuel + calculate_total_fuel(mass)
    
    return fuel

assert total_fuel("testinput.txt", True) == 34241
assert total_fuel("testinput.txt", False) == 51316

print("Part 1: %s" % (total_fuel("input.txt", True)))
print("Part 2: %s" % (total_fuel("input.txt", False)))
