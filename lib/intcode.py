def _getParameter(ip, memory, count, mode):
    """Retrieves a parameter value from memory

    Parameters:
    ip : int
        The current instruction pointer

    memory: list<int>
        The full memory of the program

    count: int
        Which parameter to retrieve (1-based)

    mode: int
        The full parameter mode provided with the operation
    """

    parameterMode = (mode // (10**(count - 1))) % 10
    if parameterMode == 0:
        return memory[memory[ip + count]]

    return memory[ip + count]

def _add(ip, memory, mode):
    """Performs an add operation."""
    if mode // 100 == 0:
        memory[memory[ip + 3]] = _getParameter(ip, memory, 1, mode) + _getParameter(ip, memory, 2, mode)
    ip = ip + 4
    return (ip, memory)

def _multiply(ip, memory, mode):
    """Performs a multipy operation."""
    if mode // 100 == 0:
        memory[memory[ip + 3]] = _getParameter(ip, memory, 1, mode) * _getParameter(ip, memory, 2, mode)
    ip = ip + 4
    return (ip, memory)

def _input(ip, memory, mode):
    """Reads input from stdin and stores it in memory"""
    if mode % 10 == 0:
        val = int(input("Please enter a number: "))
        memory[memory[ip + 1]] = val

    ip = ip + 2
    return (ip, memory)

def _output(ip, memory, mode):
    """Outputs a value from memory to stdout."""
    print("%s: %s" % (ip, _getParameter(ip, memory, 1, mode)))

    ip = ip + 2
    return (ip, memory)

def _jump_if_true(ip, memory, mode):
    """Jumps to new instruction pointer on truthy value"""
    if _getParameter(ip, memory, 1, mode) != 0:
        ip = _getParameter(ip, memory, 2, mode)
    else:
        ip = ip + 3

    return (ip, memory)

def _jump_if_false(ip, memory, mode):
    """Jumps to new instruction pointer on falsy value"""
    if _getParameter(ip, memory, 1, mode) == 0:
        ip = _getParameter(ip, memory, 2, mode)
    else:
        ip = ip + 3

    return (ip, memory)

def _less_than(ip, memory, mode):
    """Checks if first value is less than second value"""
    if mode // 100 == 0:
        if _getParameter(ip, memory, 1, mode) < _getParameter(ip, memory, 2, mode):
            memory[memory[ip + 3]] = 1
        else:
            memory[memory[ip + 3]] = 0

    ip = ip + 4
    return (ip, memory)

def _equals(ip, memory, mode):
    """Checks if two value are equal"""
    if mode // 100 == 0:
        if _getParameter(ip, memory, 1, mode) == _getParameter(ip, memory, 2, mode):
            memory[memory[ip + 3]] = 1
        else:
            memory[memory[ip + 3]] = 0

    ip = ip + 4
    return (ip, memory)

_operations = {
    1: _add,
    2: _multiply,
    3: _input,
    4: _output,
    5: _jump_if_true,
    6: _jump_if_false,
    7: _less_than,
    8: _equals
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
        opcode = memory[ip] % 100
        if opcode in _operations:
            mode = memory[ip] // 100
            ip, memory = _operations[opcode](ip, memory, mode)
        else:
            raise IndexError("Invalid opcode: %s" % opcode)

    return memory
