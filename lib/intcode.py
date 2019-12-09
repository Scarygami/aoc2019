import argparse

class State(object):
    """Representation of the current state of the Intcode application"""

    def __init__(self, ip, memory, inputs=[], outputs=[], base=0, debug=False, silent=False):
        self.ip = ip
        self.memory = [m for m in memory]
        self.inputs = [i for i in inputs]
        self.outputs = [o for o in outputs]
        self.base = base
        self.waiting = False
        self.debug = debug
        self.silent = silent

    def __repr__(self):
        return "IP: %s\nMemory: %s\nBase: %s\n" % (self.ip, self.memory, self.base)

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
            address = self.memory[self.ip + count]
        elif parameterMode == 1:
            address = self.ip + count
        elif parameterMode == 2:
            address = self.base + self.memory[self.ip + count]

        if address < len(self.memory):
            return self.memory[address]

        return 0

    def setValue(self, count, value, mode=0):
        """Sets a value in memory

        Parameters
        ----------
        count: int
            Which parameter to choose for memory address, relative to ip

        value: int
            The value to set
        """
        parameterMode = (mode // (10**(count - 1))) % 10
        if parameterMode == 0:
            address = self.memory[self.ip + count]
        elif parameterMode == 1:
            address = self.ip + count
        elif parameterMode == 2:
            address = self.base + self.memory[self.ip + count]

        while address >= len(self.memory):
            # This will most likely get me in trouble eventually...
            self.memory.append(0)

        self.memory[address] = value

def _add(state, mode):
    """Performs an add operation."""
    state.setValue(3, state.getValue(1, mode) + state.getValue(2, mode), mode)

    state.ip = state.ip + 4

def _multiply(state, mode):
    """Performs a multipy operation."""
    state.setValue(3, state.getValue(1, mode) * state.getValue(2, mode), mode)

    state.ip = state.ip + 4

def _input(state, mode):
    """Reads input from state
    If no input is available pause until resumed"""
    if len(state.inputs) > 0:
        val = state.inputs.pop(0)
    else:
        state.waiting = True
        return
    state.setValue(1, val, mode)
    state.ip = state.ip + 2

def _output(state, mode):
    """Outputs a value from memory to stdout and state."""
    val = state.getValue(1, mode)
    state.outputs.append(val)
    if not state.silent:
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
    if state.getValue(1, mode) < state.getValue(2, mode):
        state.setValue(3, 1, mode)
    else:
        state.setValue(3, 0, mode)

    state.ip = state.ip + 4

def _equals(state, mode):
    """Checks if two value are equal"""
    if state.getValue(1, mode) == state.getValue(2, mode):
        state.setValue(3, 1, mode)
    else:
        state.setValue(3, 0, mode)

    state.ip = state.ip + 4

def _adjust_base(state, mode):
    """Adjust the base for relative addresses"""
    state.base = state.base + state.getValue(1, mode)
    state.ip = state.ip + 2

_operations = {
    1: _add,
    2: _multiply,
    3: _input,
    4: _output,
    5: _jump_if_true,
    6: _jump_if_false,
    7: _less_than,
    8: _equals,
    9: _adjust_base
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

def run_intcode(memory, inputs=[], ip=0, debug=False, silent=False):
    """Runs the Intcode provided as list

    Parameters
    ----------
    memory : list<int>
        The Intcode provided as list of int values

    inputs: list<int>
        List of input values to be used for input operations (not used yet)

    ip: int
        Lets the Intcode resume from a specified instruction pointer

    debug: bool
        outputs the current state on each instruction

    silent: bool
        don't product output to stdout

    Returns the latest state after halting or pausing
    """

    state = State(ip, memory, inputs, [], 0, debug, silent)

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
            if state.waiting:
                break
        else:
            raise IndexError("Invalid opcode: %s" % opcode)

    return state

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

    machine = State(0, source, inputs)
    done = False
    while not done:
        machine = run_intcode(machine.memory, machine.inputs, machine.ip, debug, False)
        if machine.waiting:
            machine.inputs.append(int(input("Enter a number as value: ")))
        else:
            done = True

if __name__ == "__main__":
    main()
