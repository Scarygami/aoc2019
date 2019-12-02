def _add(ip, memory):
    """Performs an add operation.
    Returns the new instruction pointer and memory
    """

    memory[memory[ip + 3]] = memory[memory[ip + 1]] + memory[memory[ip + 2]]
    ip = ip + 4
    return (ip, memory)

def _multiply(ip, memory):
    """Performs a multipy operation.
    Returns the new instruction pointer and memory
    """

    memory[memory[ip + 3]] = memory[memory[ip + 1]] * memory[memory[ip + 2]]
    ip = ip + 4
    return (ip, memory)

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

    ip = 0
    while ip < len(memory) and memory[ip] != 99:
        opcode = memory[ip]
        if opcode in _operations:
            ip, memory = _operations[opcode](ip, memory)
        else:
            raise IndexError("Invalid opcode: %s" % opcode)

    return memory
