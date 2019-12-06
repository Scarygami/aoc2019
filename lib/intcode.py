import argparse

class State(object):
    """Representation of the current state of the Intcode application"""

    def __init__(self, ip, memory, inputs=[], outputs=[], debug=False):
        self.ip = ip
        self.memory = [m for m in memory]
        self.inputs = [i for i in inputs]
        self.outputs = [o for o in outputs]
        self.debug = debug

    def __repr__(self):
        return "IP: %s\nMemory: %s" % (self.ip, self.memory)

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
    if state.debug:
        print("%s: %s" % (state.ip, val))
    else:
        print("%s" % val)

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
    Also allows space-separated or newline-separated input without commas

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
            fullinput = fullinput + " " + line
        fullinput = fullinput.replace(",", " ")
        return [int(part) for part in fullinput.split(" ") if part.strip() != ""]

def run_intcode(memory, inputs=[], debug=False):
    """Runs the Intcode provided as list

    Parameters
    ----------
    memory : list<int>
        The Intcode provided as list of int values

    inputs: list<int>
        List of input values to be used for input operations (not used yet)

    Returns the latest version of the memory and the created outputs
    """

    state = State(0, memory, inputs, [], debug)

    while state.ip < len(state.memory):
        if state.debug:
            print(state)
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

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Source code in IntCode")
    parser.add_argument("-i", "--input", help="Optional file with inputs for the IntCode program, comma or whitespace separated")
    parser.add_argument("-d", "--debug", help="Whether to run the program in debug mode", action="store_true")
    args = parser.parse_args()

    source = read_intcode(args.source)

    inputs = []
    if args.input:
        inputs = read_intcode(args.input)
    debug = False
    if args.debug:
        debug = True

    run_intcode(source, inputs, debug)

if __name__ == "__main__":
    main()
