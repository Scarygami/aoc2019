import unittest
from unittest.mock import patch
import os
import sys
import contextlib
from io import StringIO

currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from lib import intcode

class TestIntCode(unittest.TestCase):
    def load_program(self, filename):
        """Helper method to load program from file"""
        return intcode.read_intcode(os.path.join(currentdir, filename))

    def test_loading(self):
        """Program should load correctly from input file"""
        program = self.load_program("testinput1.txt")
        self.assertListEqual(program, [1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50])

    def test_exception(self):
        """Incorrect Op Codes should raise an IndexError"""
        self.assertRaises(IndexError, intcode.run_intcode, [77, 0, 0, 0])

    def test_add(self):
        """Add operation should work correctly"""
        result = intcode.run_intcode([1, 5, 6, 0, 99, 10, 20]).memory
        self.assertListEqual(result, [30, 5, 6, 0, 99, 10, 20])

    def test_mulitply(self):
        """Multiply operation should work correctly"""
        result = intcode.run_intcode([2, 5, 6, 0, 99, 10, 20]).memory
        self.assertListEqual(result, [200, 5, 6, 0, 99, 10, 20])

    def test_output1(self):
        "Output operation should work correctly to stdout"""
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            intcode.run_intcode([104, 50, 99])
        self.assertEqual(temp_stdout.getvalue().strip(), "50")

    def test_output2(self):
        "Output operation should work correctly to outputs list"""
        outputs = intcode.run_intcode([104, 50, 99]).outputs

        self.assertListEqual(outputs, [50])

    def test_input(self):
        "Input operation should work correctly from inputs list"""
        result = intcode.run_intcode([3, 0, 99], [10]).memory
        self.assertListEqual(result, [10, 0, 99])

    def test_program1(self):
        """Test program 1 from AoC Day 2 should run correctly"""
        result = intcode.run_intcode(self.load_program("testinput1.txt")).memory
        self.assertListEqual(result, [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50])

    def test_program2(self):
        """Test program 2 from AoC Day 2 should run correctly"""
        result = intcode.run_intcode(self.load_program("testinput2.txt")).memory
        self.assertListEqual(result, [2, 0, 0, 0, 99])

    def test_program3(self):
        """Test program 3 from AoC Day 2 should run correctly"""
        result = intcode.run_intcode(self.load_program("testinput3.txt")).memory
        self.assertListEqual(result, [2, 3, 0, 6, 99])

    def test_program4(self):
        """Test program 4 from AoC Day 2 should run correctly"""
        result = intcode.run_intcode(self.load_program("testinput4.txt")).memory
        self.assertListEqual(result, [2, 4, 4, 5, 99, 9801])

    def test_program5(self):
        """Test program 5 from AoC Day 2 should run correctly"""
        result = intcode.run_intcode(self.load_program("testinput5.txt")).memory
        self.assertListEqual(result, [30, 1, 1, 4, 2, 5, 6, 0, 99])

    def test_program5_1(self):
        """Test program 1 from AoC Day 5 should run correctly"""
        temp_stdout = StringIO()
        with contextlib.redirect_stdout(temp_stdout):
            outputs = intcode.run_intcode([3, 0, 4, 0, 99], [17]).outputs
        self.assertListEqual(outputs, [17])

    def test_program5_2(self):
        """Test program 2 from AoC Day 5 should run correctly"""
        result = intcode.run_intcode([1002, 4, 3, 4, 33]).memory
        self.assertListEqual(result, [1002, 4, 3, 4, 99])

    def test_program5_3(self):
        """Test program 3 from AoC Day 5 should run correctly"""
        result = intcode.run_intcode([1101, 100, -1, 4, 0]).memory
        self.assertListEqual(result, [1101, 100, -1, 4, 99])

    def test_program5_4(self):
        """Test program 4 from AoC Day 5 should run correctly"""
        program = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]

        outputs = intcode.run_intcode(program, [7]).outputs
        self.assertListEqual(outputs, [0])

        outputs = intcode.run_intcode(program, [8]).outputs
        self.assertListEqual(outputs, [1])

    def test_program5_5(self):
        """Test program 5 from AoC Day 5 should run correctly"""
        program = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]

        outputs = intcode.run_intcode(program, [7]).outputs
        self.assertListEqual(outputs, [1])

        outputs = intcode.run_intcode(program, [10]).outputs
        self.assertListEqual(outputs, [0])

    def test_program5_6(self):
        """Test program 6 from AoC Day 5 should run correctly"""
        program = [3, 3, 1108, -1, 8, 3, 4, 3, 99]

        outputs = intcode.run_intcode(program, [7]).outputs
        self.assertListEqual(outputs, [0])

        outputs = intcode.run_intcode(program, [8]).outputs
        self.assertListEqual(outputs, [1])

    def test_program5_7(self):
        """Test program 7 from AoC Day 5 should run correctly"""
        program = [3, 3, 1107, -1, 8, 3, 4, 3, 99]

        outputs = intcode.run_intcode(program, [7]).outputs
        self.assertListEqual(outputs, [1])

        outputs = intcode.run_intcode(program, [10]).outputs
        self.assertListEqual(outputs, [0])

    def test_program5_8(self):
        """Test program 8 from AoC Day 5 should run correctly"""
        program = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]

        outputs = intcode.run_intcode(program, [10]).outputs
        self.assertListEqual(outputs, [1])

        outputs = intcode.run_intcode(program, [0]).outputs
        self.assertListEqual(outputs, [0])

    def test_program5_9(self):
        """Test program 9 from AoC Day 5 should run correctly"""
        program = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]

        outputs = intcode.run_intcode(program, [10]).outputs
        self.assertListEqual(outputs, [1])

        outputs = intcode.run_intcode(program, [0]).outputs
        self.assertListEqual(outputs, [0])

    def test_program5_10(self):
        """Test program 10 from AoC Day 5 should run correctly"""
        program = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                   1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                   999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]

        outputs = intcode.run_intcode(program, [10]).outputs
        self.assertListEqual(outputs, [1001])

        outputs = intcode.run_intcode(program, [8]).outputs
        self.assertListEqual(outputs, [1000])

        outputs = intcode.run_intcode(program, [1]).outputs
        self.assertListEqual(outputs, [999])

if __name__ == '__main__':
    unittest.main()
