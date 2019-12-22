import os
currentdir = os.path.dirname(os.path.abspath(__file__))


def reverse(deck):
    """deal into new stack"""
    return list(reversed(deck))


def increments(deck, N):
    """deal with increment N"""
    newdeck = [None for _ in range(len(deck))]
    for i in range(len(deck)):
        newdeck[(i * N) % len(deck)] = deck[i]
    return newdeck


def cut(deck, N):
    """cut N cards"""
    newdeck = deck[N:] + deck[:N]
    return newdeck


def shuffle(filename, cards, rounds=1):
    """shuffle specified amount of cards according to instuctions in filename
    for specified number of rounds"""

    deck = [c for c in range(cards)]
    with open(filename, "r") as f:
        instructions = f.read().splitlines()

    for _ in range(rounds):
        for instruction in instructions:
            parts = instruction.split(" ")
            if parts[0] == "cut":
                deck = cut(deck, int(parts[1]))
            elif parts[2] == "new":
                deck = reverse(deck)
            elif parts[2] == "increment":
                deck = increments(deck, int(parts[3]))
            else:
                raise Exception("Unknown instruction")

    return deck


def mod_inv(n, mod):
    """Calculates the modular multiplicative inverse of n assuming that mod is prime"""
    return pow(n, mod - 2, mod)


def calculate(filename, cards, card, rounds=1, inverse=False):
    """Calculate postion of card in shuffled cards after specified amount of rounds

    inverse=True for "unshuffling" the cards"""

    with open(filename, "r") as f:
        instructions = f.read().splitlines()

    if inverse:
        instructions.reverse()

    # shuffle(pos) = (a * pos + b) % cards
    a = 1
    b = 0
    for instruction in instructions:
        parts = instruction.split(" ")
        if parts[0] == "cut":
            if inverse:
                b = (b + int(parts[1])) % cards
            else:
                b = (b - int(parts[1])) % cards
        elif parts[2] == "new":
            a = (-a) % cards
            b = (-b - 1) % cards
        elif parts[2] == "increment":
            if inverse:
                mult = mod_inv(int(parts[3]), cards)
            else:
                mult = int(parts[3])

            a = (a * mult) % cards
            b = (b * mult) % cards
        else:
            raise Exception("Unknown instruction")

    # shuffle(pos, n) = a^n * pos + b * (a^n - 1) / (a - 1)
    a_pow = pow(a, rounds, cards)
    b_pow = (b * (a_pow - 1) * mod_inv(a - 1, cards)) % cards

    pos = (a_pow * card + b_pow) % cards

    return pos


assert shuffle(os.path.join(currentdir, "testinput1.txt"), 10) == [0, 3, 6, 9, 2, 5, 8, 1, 4, 7]
assert shuffle(os.path.join(currentdir, "testinput2.txt"), 10) == [3, 0, 7, 4, 1, 8, 5, 2, 9, 6]
assert shuffle(os.path.join(currentdir, "testinput3.txt"), 10) == [6, 3, 0, 7, 4, 1, 8, 5, 2, 9]
assert shuffle(os.path.join(currentdir, "testinput4.txt"), 10) == [9, 2, 5, 8, 1, 4, 7, 0, 3, 6]

deck = shuffle(os.path.join(currentdir, "input.txt"), 10007)
answer = deck.index(2019)
print("Part 1: %s" % answer)

assert calculate(os.path.join(currentdir, "input.txt"), 10007, 2019, 1) == answer
assert calculate(os.path.join(currentdir, "input.txt"), 10007, answer, 1, True) == 2019

print("Part 2: %s" % calculate(os.path.join(currentdir, "input.txt"), 119315717514047, 2020, 101741582076661, True))
