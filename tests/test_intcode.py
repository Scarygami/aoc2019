import unittest
import os
import sys
currentdir = os.path.dirname(os.path.abspath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0, parentdir)

from lib import intcode

class TestIntCode(unittest.TestCase):
    def load_program(self, filename):
        return intcode.read_intcode(os.path.join(currentdir, filename))

    def test_program1(self):
        result = intcode.run_intcode(self.load_program("testinput1.txt"))
        self.assertEqual(result[0], 3500)
        self.assertEqual(result[3], 70)

    def test_program2(self):
        result = intcode.run_intcode(self.load_program("testinput2.txt"))
        self.assertEqual(result[0], 2)

    def test_program3(self):
        result = intcode.run_intcode(self.load_program("testinput3.txt"))
        self.assertEqual(result[3], 6)

    def test_program4(self):
        result = intcode.run_intcode(self.load_program("testinput4.txt"))
        self.assertEqual(result[5], 9801)

    def test_program5(self):
        result = intcode.run_intcode(self.load_program("testinput5.txt"))
        self.assertEqual(result[0], 30)
        self.assertEqual(result[4], 2)

if __name__ == '__main__':
    unittest.main()
