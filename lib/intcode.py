import argparse


class IntcodeVM(object):
    """Computer executing Intcode code"""

    def __init__(self, code, debug=False, silent=False):
        """Constructor

        Parameters
        ----------
        code : list<int>
            List of Intcode

        debug : bool
            If true detailed state of the VM will be printed on each statement

        silent: bool
            If true the output statement doesn't write to stdout
        """

        self.initial_memory = {}
        for i, m in enumerate(code):
            if m != 0:
                self.initial_memory[i] = m

        self.waiting = True
        self.ip = 0
        self.base = 0
        self.inputs = []
        self.outputs = []
        self.debug = debug
        self.silent = silent

    @classmethod
    def read_intcode(cls, inputfile):
        """Reads Intcode from a file and returns a memory list.
        Can also be used for files containing input data.

        Adjusted to allow intcode in multiple lines with #-lines for comments
        Also allows space-separated or newline-separated input without commas

        Parameters
        ----------
        inputfile : str
            Name/path of file that contains the int values
        """

        with open(inputfile, "r") as f:
            fullinput = ""
            for line in f:
                if line[0] == "#":
                    continue
                fullinput = fullinput + " " + line
            fullinput = fullinput.replace(",", " ")
            return [int(part) for part in fullinput.split(" ") if part.strip() != ""]

    def copy(self):
        """Creates a new IntCode machine with exactly the same state as this one"""

        machine = IntcodeVM(self.initial_memory.copy(), self.debug, self.silent)
        machine.memory = self.memory.copy()
        machine.inputs = self.inputs.copy()
        machine.outputs = self.outputs.copy()
        machine.ip = self.ip
        machine.base = self.base
        machine.waiting = self.waiting

        return machine

    def __repr__(self):
        return "IP: %s\nMemory: %s\nBase: %s\n" % (self.ip, self.memory, self.base)

    def _getAddress(self, count, mode):
        """Determines at what address to read data based on mode

        Parameters
        ----------
        count: int
            Which parameter to retrieve (1-based), relative to ip

        mode: int
            The full parameter mode provided with the operation
        """
        parameterMode = (mode // (10**(count - 1))) % 10
        if parameterMode == 0:
            address = self.memory.get(self.ip + count, 0)
        elif parameterMode == 1:
            address = self.ip + count
        elif parameterMode == 2:
            address = self.base + self.memory.get(self.ip + count, 0)

        return address

    def _getValue(self, count, mode):
        """Retrieves a parameter value from memory

        Parameters
        ----------
        count: int
            Which parameter to retrieve (1-based), relative to ip

        mode: int
            The full parameter mode provided with the operation
        """
        address = self._getAddress(count, mode)

        return self.memory.get(address, 0)

    def _setValue(self, count, value, mode=0):
        """Sets a value in memory

        Parameters
        ----------
        count: int
            Which parameter to choose for memory address, relative to ip

        value: int
            The value to set
        """
        address = self._getAddress(count, mode)

        if value == 0:
            self.memory.pop(address, 0)
        else:
            self.memory[address] = value

    def _add(self, mode):
        """Performs an add operation."""
        self._setValue(3, self._getValue(1, mode) + self._getValue(2, mode), mode)

        self.ip = self.ip + 4

    def _multiply(self, mode):
        """Performs a multipy operation."""
        self._setValue(3, self._getValue(1, mode) * self._getValue(2, mode), mode)

        self.ip = self.ip + 4

    def _input(self, mode):
        """Reads input from state
        If no input is available pause until resumed"""
        if len(self.inputs) > 0:
            val = self.inputs.pop(0)
        else:
            self.waiting = True
            return
        self._setValue(1, val, mode)
        self.ip = self.ip + 2

    def _output(self, mode):
        """Outputs a value from memory to stdout and state."""
        val = self._getValue(1, mode)
        self.outputs.append(val)
        if not self.silent:
            if self.debug:
                print("%s: %s" % (self.ip, val))
            else:
                print("%s" % val)

        self.ip = self.ip + 2

    def _jump_if_true(self, mode):
        """Jumps to new instruction pointer on truthy value"""
        if self._getValue(1, mode) != 0:
            self.ip = self._getValue(2, mode)
        else:
            self.ip = self.ip + 3

    def _jump_if_false(self, mode):
        """Jumps to new instruction pointer on falsy value"""
        if self._getValue(1, mode) == 0:
            self.ip = self._getValue(2, mode)
        else:
            self.ip = self.ip + 3

    def _less_than(self, mode):
        """Checks if first value is less than second value"""
        if self._getValue(1, mode) < self._getValue(2, mode):
            self._setValue(3, 1, mode)
        else:
            self._setValue(3, 0, mode)

        self.ip = self.ip + 4

    def _equals(self, mode):
        """Checks if two value are equal"""
        if self._getValue(1, mode) == self._getValue(2, mode):
            self._setValue(3, 1, mode)
        else:
            self._setValue(3, 0, mode)

        self.ip = self.ip + 4

    def _adjust_base(self, mode):
        """Adjust the base for relative addresses"""
        self.base = self.base + self._getValue(1, mode)
        self.ip = self.ip + 2

    def run(self, inputs=[]):
        """Starts the program from the beginning with the initial code and memory.

        Parameters
        ----------
        inputs : list<int>
            List of input values to be used
        """
        self.ip = 0
        self.base = 0
        self.inputs = []
        self.outputs = []
        self.memory = self.initial_memory.copy()

        return self.resume(inputs)

    def resume(self, inputs=[]):
        """Resumes the program from the latest instruction pointer and state

        Parameters
        ----------
        inputs : list<int>
            List of input values to be used
        """

        self.inputs.extend(inputs)
        self.waiting = False
        self.outputs = []

        _operations = {
            1: self._add,
            2: self._multiply,
            3: self._input,
            4: self._output,
            5: self._jump_if_true,
            6: self._jump_if_false,
            7: self._less_than,
            8: self._equals,
            9: self._adjust_base
        }

        while True:
            if self.debug:
                print(self)
            op = self.memory[self.ip]
            opcode = op % 100
            if opcode == 99:
                break
            if opcode in _operations:
                mode = op // 100
                _operations[opcode](mode)
                if self.waiting:
                    break
            else:
                raise IndexError("Invalid opcode: %s" % opcode)

        return self.outputs.copy()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Source code in IntCode")
    parser.add_argument(
        "-i", "--input",
        help="Optional file with inputs for the IntCode program, comma or whitespace separated"
    )
    parser.add_argument("-d", "--debug", help="Whether to run the program in debug mode", action="store_true")
    args = parser.parse_args()

    source = IntcodeVM.read_intcode(args.source)

    inputs = []
    if args.input:
        inputs = IntcodeVM.read_intcode(args.input)
    debug = False
    if args.debug:
        debug = True

    machine = IntcodeVM(source, debug)
    while machine.waiting:
        machine.run(inputs)
        if machine.waiting:
            value = int(input("Enter a number as value: "))
            machine.resume([value])


if __name__ == "__main__":
    main()
