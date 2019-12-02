def _add(ic, memory):
    """Performs an add operation.
    Returns the new instruction counter and memory
    """

    memory[memory[ic + 3]] = memory[memory[ic + 1]] + memory[memory[ic + 2]]
    ic = ic + 4
    return (ic, memory)

def _multiply(ic, memory):
    """Performs a multipy operation.
    Returns the new instruction counter and memory
    """

    memory[memory[ic + 3]] = memory[memory[ic + 1]] * memory[memory[ic + 2]]
    ic = ic + 4
    return (ic, memory)

_operations = {
    1: _add,
    2: _multiply
}

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
    """Runs the Intcode provided as list

    Parameters
    ----------
    memory : list<int>
        The Intcode provided as list of int values
    """

    ic = 0
    while ic < len(memory) and memory[ic] != 99:
        opcode = memory[ic]
        if opcode in _operations:
            ic, memory = _operations[opcode](ic, memory)
        else:
            raise Exception("Invalid opcode: %s" % opcode)

    return memory
