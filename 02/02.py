def run_intcode(inputfile, noun=None, verb=None):
    """Runs the Intcode provided in inputfile

    Parameters
    ----------
    inputfile : str
        Name/path of file that contains the puzzle input

    noun : int
        Fixed value to put into memory[1]

    verb : int
        Fixed value to put into memory[2]
    """

    with open(inputfile, "r") as f:
        memory = [int(part) for part in f.readline().split(",")]

    if noun is not None:
        memory[1] = noun
    if verb is not None:
        memory[2] = verb

    ic = 0
    while ic < len(memory) and memory[ic] != 99:
        opcode = memory[ic]

        if opcode == 1:
            parameters = 3
            memory[memory[ic + 3]] = memory[memory[ic + 1]] + memory[memory[ic + 2]]
        elif opcode == 2:
            parameters = 3
            memory[memory[ic + 3]] = memory[memory[ic + 1]] * memory[memory[ic + 2]]
        else:
            raise Exception("Invalid opcode: %s" % opcode)

        ic = ic + parameters + 1

    return memory


test_result1 = run_intcode("testinput1.txt")
assert test_result1[0] == 3500
assert test_result1[3] == 70

test_result2 = run_intcode("testinput2.txt")
assert test_result2[0] == 2

test_result3 = run_intcode("testinput3.txt")
assert test_result3[3] == 6

test_result4 = run_intcode("testinput4.txt")
assert test_result4[5] == 9801

test_result5 = run_intcode("testinput5.txt")
assert test_result5[0] == 30
assert test_result5[4] == 2


result = run_intcode("input.txt", 12, 2)
print("Part 1: %s" % (result[0]))

# Brute-forcing part 2, because too lazy to reverse-engineer the intcode
for noun in range(0, 100):
    for verb in range(0, 100):
        if run_intcode("input.txt", noun, verb)[0] == 19690720:
            print("Part 2: %s" % (100 * noun + verb))
            exit(0)
