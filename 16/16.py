import os
import math
from time import time

currentdir = os.path.dirname(os.path.abspath(__file__))


def create_pattern(index):
    base_pattern = [0, 1, 0, -1]
    repeat = index + 1
    pattern = []
    for p in base_pattern:
        pattern.extend([p] * repeat)

    pattern.append(pattern.pop(0))

    return pattern


def fft(signal, phases):
    patterns = {}
    middle = len(signal) // 2

    for _ in range(phases):
        new_signal = []

        for position in range(middle):
            if position not in patterns:
                patterns[position] = create_pattern(position)
            pattern = patterns[position]

            new_value = sum(v * pattern[(p + position) % len(pattern)] for p, v in enumerate(signal[position:]))
            new_signal.append(abs(new_value) % 10)

        second_half = fake_fft(signal, 1, middle)
        new_signal.extend(second_half)

        signal = new_signal

    return signal


def fake_fft(signal, phases=1, offset=0):
    """Beyond the halfway point the new value is always the sum of all items starting from position"""

    signal = signal[offset:]
    for _ in range(phases):
        value = 0
        new_signal = []
        for _ in range(len(signal)):
            value = (value + signal.pop()) % 10
            new_signal.append(value)

        new_signal.reverse()
        signal = new_signal

    return signal


def decode_message(signal, phases, real_signal=False):
    if real_signal:
        offset = sum(v * 10 ** (6 - p) for p, v in enumerate(signal[0: 7]))
        signal = signal * 10000
        if (offset < len(signal) // 2):
            raise NotImplementedError
        decoded_signal = fake_fft(signal, phases, offset)
    else:
        decoded_signal = fft(signal, phases)

    return "".join(map(lambda x: str(x), decoded_signal[0: 8]))


def decode_file(filename, phases, real_signal=False):
    with open(filename, "r") as f:
        line = f.read().splitlines()[0]

    signal = [int(c) for c in line]

    return decode_message(signal, phases, real_signal)


assert decode_message([1, 2, 3, 4, 5, 6, 7, 8], 1) == "48226158"
assert decode_message([1, 2, 3, 4, 5, 6, 7, 8], 2) == "34040438"
assert decode_message([1, 2, 3, 4, 5, 6, 7, 8], 3) == "03415518"
assert decode_message([1, 2, 3, 4, 5, 6, 7, 8], 4) == "01029498"

assert decode_file(os.path.join(currentdir, "testinput1.txt"), 100) == "24176176"
assert decode_file(os.path.join(currentdir, "testinput2.txt"), 100) == "73745418"
assert decode_file(os.path.join(currentdir, "testinput3.txt"), 100) == "52432133"

start = time()
result = decode_file(os.path.join(currentdir, "input.txt"), 100)
end = time()
print("Part 1: %s (%.2f s)" % (result, end - start))

assert decode_file(os.path.join(currentdir, "testinput4.txt"), 100, True) == "84462026"
assert decode_file(os.path.join(currentdir, "testinput5.txt"), 100, True) == "78725270"
assert decode_file(os.path.join(currentdir, "testinput6.txt"), 100, True) == "53553731"

start = time()
result = decode_file(os.path.join(currentdir, "input.txt"), 100, True)
end = time()
print("Part 2: %s (%.2f s)" % (result, end - start))
