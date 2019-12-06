class State(object):
    """Representation of the current state of the Intcode application"""

    def __init__(self, ip, memory, inputs=[], outputs=[]):
        self.ip = ip
        self.memory = [m for m in memory]
        self.inputs = [i for i in inputs]
        self.outputs = [o for o in outputs]

    def getValue(self, count, mode):
        """Retrieves a parameter value from memory

        Parameters
        ----------
        count: int
            Which parameter to retrieve (1-based), relative to ip

        mode: int
            The full parameter mode provided with the operation
        """
        parameterMode = (mode // (10**(count - 1))) % 10
        if parameterMode == 0:
            return self.memory[self.memory[self.ip + count]]

        return self.memory[self.ip + count]

    def setValue(self, count, value):
        """Sets a value in memory

        Parameters
        ----------
        count: int
            Which parameter to choose for memory address, relative to ip
        
        value: int
            The value to set
        """
        self.memory[self.memory[self.ip + count]] = value

def _add(state, mode):
    """Performs an add operation."""
    if mode // 100 == 0:
        state.setValue(3, state.getValue(1, mode) + state.getValue(2, mode))

    state.ip = state.ip + 4

def _multiply(state, mode):
    """Performs a multipy operation."""
    if mode // 100 == 0:
        state.setValue(3, state.getValue(1, mode) * state.getValue(2, mode))

    state.ip = state.ip + 4

def _input(state, mode):
    """Reads input from state or stdin and stores it in memory"""
    if mode % 10 == 0:
        if len(state.inputs) > 0:
            val = state.inputs.pop(0)
        else:
            val = int(input("Please enter a number: "))
        state.setValue(1, val)

    state.ip = state.ip + 2

def _output(state, mode):
    """Outputs a value from memory to stdout and state."""
    val = state.getValue(1, mode)
    state.outputs.append(val)
    print("%s: %s" % (state.ip, val))

    state.ip = state.ip + 2

def _jump_if_true(state, mode):
    """Jumps to new instruction pointer on truthy value"""
    if state.getValue(1, mode) != 0:
        state.ip = state.getValue(2, mode)
    else:
        state.ip = state.ip + 3

def _jump_if_false(state, mode):
    """Jumps to new instruction pointer on falsy value"""
    if state.getValue(1, mode) == 0:
        state.ip = state.getValue(2, mode)
    else:
        state.ip = state.ip + 3

def _less_than(state, mode):
    """Checks if first value is less than second value"""
    if mode // 100 == 0:
        if state.getValue(1, mode) < state.getValue(2, mode):
            state.setValue(3, 1)
        else:
            state.setValue(3, 0)

    state.ip = state.ip + 4

def _equals(state, mode):
    """Checks if two value are equal"""
    if mode // 100 == 0:
        if state.getValue(1, mode) == state.getValue(2, mode):
            state.setValue(3, 1)
        else:
            state.setValue(3, 0)

    state.ip = state.ip + 4

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

    Adjusted to allow intcode in multiple lines with #-lines for comments

    Parameters
    ----------
    inputfile : str
        Name/path of file that contains the Intcode
    """

    with open(inputfile, "r") as f:
        fullinput = ""
        for line in f:
            if line[0] == "#":
                continue
            fullinput = fullinput + line
        return [int(part) for part in fullinput.split(",")]

def run_intcode(memory, inputs = []):
    """Runs the Intcode provided as list

    Parameters
    ----------
    memory : list<int>
        The Intcode provided as list of int values

    inputs: list<int>
        List of input values to be used for input operations (not used yet)

    Returns the latest version of the memory and the created outputs
    """

    state = State(0, memory, inputs, [])

    while state.ip < len(state.memory):
        op = state.memory[state.ip]
        opcode = op % 100
        if opcode == 99:
            break
        if opcode in _operations:
            mode = op // 100
            _operations[opcode](state, mode)
        else:
            raise IndexError("Invalid opcode: %s" % opcode)

    return (state.memory, state.outputs)
