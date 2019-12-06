import argparse

VARIABLE = 1
JUMPPOINT= 2

# "asm code" : (intcode, number of parameters, type of parameter, ...)
operations = {
    "add": (1, 3, VARIABLE, VARIABLE, VARIABLE),
    "mul": (2, 3, VARIABLE, VARIABLE, VARIABLE),
    "in": (3, 1, VARIABLE),
    "out": (4, 1, VARIABLE),
    "jit": (5, 2, VARIABLE, JUMPPOINT),
    "jif": (6, 2, VARIABLE, JUMPPOINT),
    "lt": (7, 3, VARIABLE, VARIABLE, VARIABLE),
    "eq": (8, 3, VARIABLE, VARIABLE, VARIABLE),
    "halt": (99, 0)
}

def isInt(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def parseOperation(line, variables):
    intcode = []
    line = line.replace(",", " ")
    parts = [part.strip() for part in line.split(" ") if part.strip() != ""]

    if parts[0] not in operations:
        raise SyntaxError("Unknown operation %s." % parts[0])

    operation = operations[parts[0]]
    intcode.append(operation[0])

    if len(parts) - 1 != operation[1]:
        raise SyntaxError("Operation %s expects %s parameters, %s found." % (parts[0], operation[1], len(parts) - 1))

    mode = 0
    for x in range(len(parts) - 1):
        if operation[x + 2] == VARIABLE:
            if isInt(parts[x + 1]):
                mode = mode + 10**x
                intcode.append(int(parts[x + 1]))
            else:
                intcode.append((VARIABLE, parts[x + 1]))
                variables[parts[x + 1]] = 0
        else:
            mode = mode + 10**x
            intcode.append((JUMPPOINT, parts[x + 1]))

    intcode[0] = 100 * mode + intcode[0]

    return intcode

def compile(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f.read().splitlines()]

    intcode = []
    jumppoints = {}
    variables = {}

    # Step 1: parse code
    for line in lines:
        ip = len(intcode)
        if line[0] == "#":
            # Skip comments
            continue

        if line[-1] == ":":
            jp = line[:-1]
            if jp in jumppoints:
                raise SyntaxError("Duplicate jump point %s is not possible." % jp)
            jumppoints[jp] = ip
        else:
            intcode.extend(parseOperation(line, variables))
            pass

    # Step 2: resolve variable and jumppoint references
    intcode = [jumppoints[x[1]] if type(x) is tuple and x[0] == JUMPPOINT else x for x in intcode]

    for variable in variables:
        ip = len(intcode)
        intcode.append(0)
        variables[variable] = ip

    intcode = [variables[x[1]] if type(x) is tuple and x[0] == VARIABLE else x for x in intcode]

    return intcode

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Input file in IntCode-Assembler language")
    parser.add_argument("output", help="Generated output file in compiled IntCode (will be overwritten)")
    args = parser.parse_args()

    if args.input == args.output:
        parser.error("Input and output have to be different files")
        return

    intcode = compile(args.input)

    with open(args.output, "w") as f:
        f.write(",".join([str(i) for i in intcode]))

if __name__ == "__main__":
    main()
