# [Day 1: The Tyranny of the Rocket Equation](https://adventofcode.com/2019/day/1)

The IntCode implementation of Part 1 can be started using my interpreter with run_ic01.py

Or you can run it using lib/intcode.py directly

    python intcode.py path/to/01_part1.ic -i path/to/01_input_file

The input file in this case needs to have an extra 0 at the end to tell IntCode that no more values are to be expected.

You can use the [ic_compiler.py](https://github.com/Scarygami/aoc2019/blob/master/ic_compiler/) to translate my syntax of IntCode-Assembler Language ([Sample](https://github.com/Scarygami/aoc2019/blob/master/01/01_part1.icasm)) to pure Intcode.
