import unittest
from src.test import add_two_numbers


class TestAddTwoNumbers(unittest.TestCase):
    def test_positive_numbers(self):
        self.assertEqual(add_two_numbers(2, 3), 5)

    def test_negative_numbers(self):
        self.assertEqual(add_two_numbers(-2, -3), -5)

    def test_mixed_numbers(self):
        self.assertEqual(add_two_numbers(-2, 3), 1)

    def test_zero(self):
        self.assertEqual(add_two_numbers(0, 0), 0)

if __name__ == '__main__':
    unittest.main()