# Advent of Code 2019 / IntCode Compiler

Very simplistic compiler from IntCode-asm to IntCode.

[Sample icasm file](https://github.com/Scarygami/aoc2019/blob/master/01/01_part1.icasm)

### Assembly syntax

Maximum of one command per line.

Each line can have one jump entry point at the beginning separated with a `:` from the command.

    <jp>: <command>

Comments can be added starting with a `#` all text after a `#` will be ignored in this line

    <command> # I am a comment

Variable names and jump point names, can be any non-numeric string and are case-sensitive.

Numeric values will be handled as direct inputs to the commands.

### Commands

##### `add <value1|variable1> <value2|variable2> <variable3>`

Calculates the sum of the first two parameters and stores it in `variable3`.

##### `mul <value1|variable1> <value2|variable2> <variable3>`

Calculates the product of the first two parameters and stores it in `variable3`.

##### `in <variable>`

Reads a value from provided input (or stdin) and stores it in `variable`.

##### `out <value|variable>`

Outputs the specified value.

##### `jit <value|variable> <destination>`

If the specified value is true (i.e. not zero) program will continue from the specified `destination` jump point.

##### `jif <value|variable> <destination>`

If the specified value is false (i.e. zero) program will continue from the specified `destination` jump point.

##### `lt <value1|variable1> <value2|variable2> <variable3>`

If the first parameter is less than the second parameter, `variable3` will be set to 1, otherwise to 0.

##### `eq <value1|variable1> <value2|variable2> <variable3>`

If the first parameter is equal the second parameter, `variable3` will be set to 1, otherwise to 0.

##### `halt`

Program ends immediately.
