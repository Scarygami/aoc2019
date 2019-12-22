import os
currentdir = os.path.dirname(os.path.abspath(__file__))


def _reverse(deck):
    return list(reversed(deck))


def _increments(deck, amount):
    newdeck = [None for _ in range(len(deck))]
    for i in range(len(deck)):
        newdeck[(i * amount) % len(deck)] = deck[i]
    return newdeck


def _cut(deck, amount):
    newdeck = deck[amount:]
    newdeck.extend(deck[:amount])
    return newdeck


def shuffle(filename, cards):
    deck = [c for c in range(cards)]
    with open(filename, "r") as f:
        instructions = f.read().splitlines()

    for instruction in instructions:
        parts = instruction.split(" ")
        if parts[0] == "cut":
            deck = _cut(deck, int(parts[1]))
        elif parts[2] == "new":
            deck = _reverse(deck)
        elif parts[2] == "increment":
            deck = _increments(deck, int(parts[3]))
        else:
            raise Exception("Unknown instruction")

    return deck


def calculate(filename, cards, card, rounds=1):
    # Calculate postion of card in shuffled cards
    with open(filename, "r") as f:
        instructions = f.read().splitlines()

    a = 1
    b = 0
    for instruction in instructions:
        parts = instruction.split(" ")
        if parts[0] == "cut":
            b = (b - int(parts[1])) % cards
        elif parts[2] == "new":
            a = (-a) % cards
            b = (-b - 1) % cards
        elif parts[2] == "increment":
            a = (a * int(parts[3])) % cards
            b = (b * int(parts[3])) % cards
        else:
            raise Exception("Unknown instruction")

    pos = card
    a_pow = pow(a, rounds, cards)
    b_pow = (b * (a_pow - 1) * mod_inv(a - 1, cards)) % cards

    pos = (a_pow * card + b_pow) % cards

    return pos


def mod_inv(n, mod):
    return pow(n, mod - 2, mod)


def calculate_inv(filename, cards, pos, rounds=1):
    # Calculate card that is in postion of shuffled cards
    with open(filename, "r") as f:
        instructions = reversed(f.read().splitlines())

    a = 1
    b = 0
    for instruction in instructions:
        parts = instruction.split(" ")
        if parts[0] == "cut":
            b = (b + int(parts[1])) % cards
        elif parts[2] == "new":
            a = (-a) % cards
            b = (-b - 1) % cards
        elif parts[2] == "increment":
            inv = mod_inv(int(parts[3]), cards)
            a = (a * inv) % cards
            b = (b * inv) % cards
        else:
            raise Exception("Unknown instruction")

    a_pow = pow(a, rounds, cards)
    b_pow = (b * (a_pow - 1) * mod_inv(a - 1, cards)) % cards

    card = (a_pow * pos + b_pow) % cards

    return card


assert shuffle(os.path.join(currentdir, "testinput1.txt"), 10) == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
assert shuffle(os.path.join(currentdir, "testinput2.txt"), 10) == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]
assert shuffle(os.path.join(currentdir, "testinput3.txt"), 10) == [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]
assert shuffle(os.path.join(currentdir, "testinput4.txt"), 10) == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]

deck = shuffle(os.path.join(currentdir, "input.txt"), 10007)
print("Part 1: %s" % deck.index(2019))

assert calculate(os.path.join(currentdir, "input.txt"), 10007, 2019, 1) == 2496
assert calculate_inv(os.path.join(currentdir, "input.txt"), 10007, 2496, 1) == 2019

print("Part 2: %s" % calculate_inv(os.path.join(currentdir, "input.txt"), 119315717514047, 2020, 101741582076661))
