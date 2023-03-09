import unittest
from calculator import Calculator
import math


class ApplicationTest(unittest.TestCase):
    add_list = [[1, 2, 3], [2, 1, 3], [6, 6, 12], [5, 9, 14],
                [205, 295, 500]]
    divide_list = [[37249, 193, 193], [36, 6, 6], [1, -1, -1], [-1, 1, -1],
                   [-1, -1, 1]]
    sqrt_list = [[4, 2], [225, 15], [289, 17], [6.25, 2.5], [324, 18]]
    exp_list = [[18, math.exp(18)], [401, math.exp(401)], [11, math.exp(11)],
                [6, math.exp(6)], [0, 1]]

    def test_add(self):
        for a, b, ans in self.add_list:
            self.assertEqual(Calculator.add(a, b), ans)

        with self.assertRaises(TypeError):
            Calculator.add(66, '6')

    def test_divide(self):
        for a, b, ans in self.divide_list:
            self.assertEqual(Calculator.divide(a, b), ans)

        with self.assertRaises(ZeroDivisionError):
            Calculator.divide(31155017, 0)

    def test_sqrt(self):
        for a, ans in self.sqrt_list:
            self.assertEqual(Calculator.sqrt(a), ans)

        with self.assertRaises(ValueError):
            Calculator.sqrt(-1)

    def test_exp(self):
        for a, ans in self.exp_list:
            self.assertEqual(Calculator.exp(a), ans)

        with self.assertRaises(OverflowError):
            Calculator.exp(10000000)


if __name__ == '__main__':
    unittest.main()
