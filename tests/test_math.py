import unittest
import os
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

    def test_large_numbers(self):
        self.assertEqual(add_two_numbers(1000000, 2000000), 3000000)

    def test_type_error(self):
        with self.assertRaises(TypeError):
            add_two_numbers("2", 3)
            
    def test_value_env(self):
        self.assertEqual(os.environ['GIT_HUB_KEY'], 'Pi')
        
        
        
        
        

if __name__ == '__main__':
    unittest.main()
