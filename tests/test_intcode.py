import unittest
import os
import sys
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
        self.assertRaises(IndexError, intcode.run_intcode, [5, 0, 0, 0])

    def test_add(self):
        """Add operation should work correclty"""
        ic, memory = intcode._add(0, [1, 4, 5, 0, 10, 20])
        self.assertEqual(ic, 4)
        self.assertListEqual(memory, [30, 4, 5, 0, 10, 20])

    def test_mulitply(self):
        """Multipy operation should work correclty"""
        ic, memory = intcode._multiply(0, [2, 4, 5, 0, 10, 20])
        self.assertEqual(ic, 4)
        self.assertListEqual(memory, [200, 4, 5, 0, 10, 20])

    def test_program1(self):
        """Test program 1 from AoC Day 2 should run correctly"""
        result = intcode.run_intcode(self.load_program("testinput1.txt"))
        self.assertListEqual(result, [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50])

    def test_program2(self):
        """Test program 2 from AoC Day 2 should run correctly"""
        result = intcode.run_intcode(self.load_program("testinput2.txt"))
        self.assertListEqual(result, [2, 0, 0, 0, 99])

    def test_program3(self):
        """Test program 3 from AoC Day 2 should run correctly"""
        result = intcode.run_intcode(self.load_program("testinput3.txt"))
        self.assertListEqual(result, [2, 3, 0, 6, 99])

    def test_program4(self):
        """Test program 4 from AoC Day 2 should run correctly"""
        result = intcode.run_intcode(self.load_program("testinput4.txt"))
        self.assertListEqual(result, [2, 4, 4, 5, 99, 9801])

    def test_program5(self):
        """Test program 5 from AoC Day 2 should run correctly"""
        result = intcode.run_intcode(self.load_program("testinput5.txt"))
        self.assertListEqual(result, [30, 1, 1, 4, 2, 5, 6, 0, 99])

if __name__ == '__main__':
    unittest.main()
