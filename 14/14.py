import os
import math
currentdir = os.path.dirname(os.path.abspath(__file__))


def read_instructions(filename):
    instructions = {}
    with open(filename, "r") as f:
        for line in f.read().splitlines():
            reactants, product = [part.strip() for part in line.split("=>")]
            reactants = [reactant.strip().split(" ") for reactant in reactants.split(",")]
            reactants = [(int(reactant[0]), reactant[1]) for reactant in reactants]
            amount, product = product.split(" ")
            amount = int(amount)
            instructions[product] = (amount, reactants)

    return instructions


def fuel_requirements(instructions, fuel=1):
    products = {"FUEL": fuel}
    ore = 0
    extras = {}

    while len(products) > 0:
        product, amount = products.popitem()
        instruction_amount, reactants = instructions[product]
        multiplicator = int(math.ceil(amount / instruction_amount))
        extras[product] = extras.get(product, 0) + instruction_amount * multiplicator - amount

        for reactant_amount, reactant in reactants:
            necessary = multiplicator * reactant_amount

            if reactant == "ORE":
                ore = ore + necessary
                continue

            # Use up any extras from previous reactions
            extra = extras.get(reactant, 0)
            extras[reactant] = max(extra - necessary, 0)
            necessary = max(necessary - extra, 0)
            if necessary == 0:
                continue

            products[reactant] = products.get(reactant, 0) + necessary

    return ore


def part1(filename):
    instructions = read_instructions(filename)
    return fuel_requirements(instructions, 1)


def maximum_fuel(filename, ore=1000000000000):
    instructions = read_instructions(filename)

    # find an upper limit
    min_fuel = 1
    max_fuel = 1
    while fuel_requirements(instructions, max_fuel) < ore:
        max_fuel = max_fuel * 2

    # Binary search
    while True:
        fuel = min_fuel + (max_fuel - min_fuel) // 2
        necessary_ore = fuel_requirements(instructions, fuel)

        if necessary_ore <= ore:
            min_fuel = fuel
        if necessary_ore >= ore:
            max_fuel = fuel

        if (max_fuel - min_fuel) <= 1:
            return min_fuel


assert part1(os.path.join(currentdir, "testinput1.txt")) == 31
assert part1(os.path.join(currentdir, "testinput2.txt")) == 165
assert part1(os.path.join(currentdir, "testinput3.txt")) == 13312
assert part1(os.path.join(currentdir, "testinput4.txt")) == 180697
assert part1(os.path.join(currentdir, "testinput5.txt")) == 2210736

print("Part 1: %s" % part1(os.path.join(currentdir, "input.txt")))

assert maximum_fuel(os.path.join(currentdir, "testinput3.txt")) == 82892753
assert maximum_fuel(os.path.join(currentdir, "testinput4.txt")) == 5586022
assert maximum_fuel(os.path.join(currentdir, "testinput5.txt")) == 460664

print("Part 2: %s" % maximum_fuel(os.path.join(currentdir, "input.txt")))
