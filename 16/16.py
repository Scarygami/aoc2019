import os
import math
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

            new_value = sum(v * pattern[p % len(pattern)] for p, v in enumerate(signal))
            new_signal.append(abs(new_value) % 10)

        second_half = fake_fft(signal, 1, middle)
        new_signal.extend(second_half)

        signal = new_signal

    return signal[0:8]


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


def decode_message(signal, phases):
    offset = sum(v * 10 ** (6 - p) for p, v in enumerate(signal[0: 7]))
    signal = signal * 10000
    if (offset < len(signal) // 2):
        raise NotImplementedError

    decoded_signal = fake_fft(signal, phases, offset)
    return decoded_signal[0: 8]


def fft_from_file(filename, phases, real_signal=False):
    with open(filename, "r") as f:
        line = f.read().splitlines()[0]

    signal = [int(c) for c in line]

    if real_signal:
        return decode_message(signal, phases)
    else:
        return fft(signal, phases)


assert fft([1, 2, 3, 4, 5, 6, 7, 8], 1) == [4, 8, 2, 2, 6, 1, 5, 8]
assert fft([1, 2, 3, 4, 5, 6, 7, 8], 2) == [3, 4, 0, 4, 0, 4, 3, 8]
assert fft([1, 2, 3, 4, 5, 6, 7, 8], 3) == [0, 3, 4, 1, 5, 5, 1, 8]
assert fft([1, 2, 3, 4, 5, 6, 7, 8], 4) == [0, 1, 0, 2, 9, 4, 9, 8]

assert fft_from_file(os.path.join(currentdir, "testinput1.txt"), 100) == [2, 4, 1, 7, 6, 1, 7, 6]
assert fft_from_file(os.path.join(currentdir, "testinput2.txt"), 100) == [7, 3, 7, 4, 5, 4, 1, 8]
assert fft_from_file(os.path.join(currentdir, "testinput3.txt"), 100) == [5, 2, 4, 3, 2, 1, 3, 3]

print("Part 1: ", fft_from_file(os.path.join(currentdir, "input.txt"), 100))

assert fft_from_file(os.path.join(currentdir, "testinput4.txt"), 100, True) == [8, 4, 4, 6, 2, 0, 2, 6]
assert fft_from_file(os.path.join(currentdir, "testinput5.txt"), 100, True) == [7, 8, 7, 2, 5, 2, 7, 0]
assert fft_from_file(os.path.join(currentdir, "testinput6.txt"), 100, True) == [5, 3, 5, 5, 3, 7, 3, 1]

print("Part 2: ", fft_from_file(os.path.join(currentdir, "input.txt"), 100, True))
