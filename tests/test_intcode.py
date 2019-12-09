import unittest
from unittest.mock import patch
import os
import sys
import contextlib
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from lib.intcode import IntcodeVM

class TestIntCode(unittest.TestCase):
    def run_program(self, code, inputs=[]):
        """Helper method to initialise an IntcodeVM,
        run it and return the machine itself and the output of the run"""
        machine = IntcodeVM(code)
        outputs = machine.run(inputs)
        return machine, outputs

    def test_loading(self):
        """Program should load correctly from input file"""
        program = IntcodeVM.read_intcode(os.path.join(currentdir, "testinput1.txt"))
        self.assertListEqual(program, [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])

    def test_exception(self):
        """Incorrect Op Codes should raise an IndexError"""
        self.assertRaises(IndexError, self.run_program, [77, 0, 0, 0])

    def test_add(self):
        """Add operation should work correctly"""
        machine, _ = self.run_program([1, 5, 6, 0, 99, 10, 20])
        self.assertEqual(machine.memory[0], 30)

    def test_mulitply(self):
        """Multiply operation should work correctly"""
        machine, _ = self.run_program([2, 5, 6, 0, 99, 10, 20])
        self.assertEqual(machine.memory[0], 200)

    def test_output(self):
        """Output operation should work correctly"""
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            _, outputs = self.run_program([104, 50, 99])
        self.assertEqual(temp_stdout.getvalue().strip(), "50")
        self.assertListEqual(outputs, [50])

    def test_input(self):
        """Input operation should work correctly from inputs list"""
        machine, _ = self.run_program([3, 0, 99], [10])
        self.assertEqual(machine.memory[0], 10)

    def test_no_input(self):
        """Machine should stop with waiting state if input is missing"""
        machine, _ = self.run_program([3, 0, 99])
        self.assertTrue(machine.waiting)

    def test_program2_1(self):
        """Test program 1 from AoC Day 2 should run correctly"""
        machine, _ = self.run_program([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])
        self.assertEqual(machine.memory[3], 70)
        self.assertEqual(machine.memory[0], 3500)

    def test_program2_2(self):
        """Test program 2 from AoC Day 2 should run correctly"""
        machine, _ = self.run_program([1, 0, 0, 0, 99])
        self.assertEqual(machine.memory[0], 2)

    def test_program2_3(self):
        """Test program 3 from AoC Day 2 should run correctly"""
        machine, _ = self.run_program([2, 3, 0, 3, 99])
        self.assertEqual(machine.memory[3], 6)

    def test_program2_4(self):
        """Test program 4 from AoC Day 2 should run correctly"""
        machine, _ = self.run_program([2, 4, 4, 5, 99, 0])
        self.assertEqual(machine.memory[5], 9801)

    def test_program2_5(self):
        """Test program 5 from AoC Day 2 should run correctly"""
        machine, _ = self.run_program([1, 1, 1, 4, 99, 5, 6, 0, 99])
        self.assertEqual(machine.memory[4], 2)
        self.assertEqual(machine.memory[0], 30)

    def test_program5_1(self):
        """Test program 1 from AoC Day 5 should run correctly"""
        _, outputs = self.run_program([3, 0, 4, 0, 99], [17])
        self.assertListEqual(outputs, [17])

    def test_program5_2(self):
        """Test program 2 from AoC Day 5 should run correctly"""
        machine, _ = self.run_program([1002, 4, 3, 4, 33])
        self.assertEqual(machine.memory[4], 99)

    def test_program5_3(self):
        """Test program 3 from AoC Day 5 should run correctly"""
        machine, _ = self.run_program([1101, 100, -1, 4, 0])
        self.assertEqual(machine.memory[4], 99)

    def test_program5_4(self):
        """Test program 4 from AoC Day 5 should run correctly"""
        program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]

        _, outputs = self.run_program(program, [7])
        self.assertListEqual(outputs, [0])

        _, outputs = self.run_program(program, [8])
        self.assertListEqual(outputs, [1])

    def test_program5_5(self):
        """Test program 5 from AoC Day 5 should run correctly"""
        program = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]

        _, outputs = self.run_program(program, [7])
        self.assertListEqual(outputs, [1])

        _, outputs = self.run_program(program, [10])
        self.assertListEqual(outputs, [0])

    def test_program5_6(self):
        """Test program 6 from AoC Day 5 should run correctly"""
        program = [3, 3, 1108, -1, 8, 3, 4, 3, 99]

        _, outputs = self.run_program(program, [7])
        self.assertListEqual(outputs, [0])

        _, outputs = self.run_program(program, [8])
        self.assertListEqual(outputs, [1])

    def test_program5_7(self):
        """Test program 7 from AoC Day 5 should run correctly"""
        program = [3, 3, 1107, -1, 8, 3, 4, 3, 99]

        _, outputs = self.run_program(program, [7])
        self.assertListEqual(outputs, [1])

        _, outputs = self.run_program(program, [10])
        self.assertListEqual(outputs, [0])

    def test_program5_8(self):
        """Test program 8 from AoC Day 5 should run correctly"""
        program = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]

        _, outputs = self.run_program(program, [10])
        self.assertListEqual(outputs, [1])

        _, outputs = self.run_program(program, [0])
        self.assertListEqual(outputs, [0])

    def test_program5_9(self):
        """Test program 9 from AoC Day 5 should run correctly"""
        program = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]

        _, outputs = self.run_program(program, [10])
        self.assertListEqual(outputs, [1])

        _, outputs = self.run_program(program, [0])
        self.assertListEqual(outputs, [0])

    def test_program5_10(self):
        """Test program 10 from AoC Day 5 should run correctly"""
        program = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                   1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                   999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]

        _, outputs = self.run_program(program, [10])
        self.assertListEqual(outputs, [1001])

        _, outputs = self.run_program(program, [8])
        self.assertListEqual(outputs, [1000])

        _, outputs = self.run_program(program, [1])
        self.assertListEqual(outputs, [999])

    def test_program9_1(self):
        """test program 1 from AoC Day 9 should run correctly"""
        program = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
        _, outputs = self.run_program(program)
        self.assertListEqual(program, outputs)

    def test_program9_2(self):
        """test program 1 from AoC Day 9 should run correctly"""
        _, outputs = self.run_program([1102,34915192,34915192,7,4,7,99,0])
        self.assertEqual(outputs.pop(), 1219070632396864)

    def test_program9_3(self):
        """test program 1 from AoC Day 9 should run correctly"""
        _, outputs = self.run_program([104,1125899906842624,99])
        self.assertEqual(outputs.pop(), 1125899906842624)

if __name__ == '__main__':
    unittest.main()
