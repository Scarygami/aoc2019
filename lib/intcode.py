def read_intcode(inputfile):
    """Reads Intcode from a file and returns a memory list

    Parameters
    ----------
    inputfile : str
        Name/path of file that contains the Intcode
    """
    with open(inputfile, "r") as f:
        return [int(part) for part in f.readline().split(",")]

def run_intcode(memory):
    """Runs the Intcode provided in inputfile

    Parameters
    ----------
    memory : list<int>
        The Intcode provided as list of int values

    """
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
