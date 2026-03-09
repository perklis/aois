import unittest
from BCD2421Calculator import BCD2421Calculator
from exceptions import BCD2421Error

class TestBCD2421Calculator(unittest.TestCase):
    def setUp(self):
        self.calc = BCD2421Calculator()

    def test_digits_to_bits_single_digit(self):
        self.assertEqual(self.calc.digits_to_bits([0]), [0, 0, 0, 0])
        self.assertEqual(self.calc.digits_to_bits([5]), [1, 0, 1, 1])
        self.assertEqual(self.calc.digits_to_bits([9]), [1, 1, 1, 1])

    def test_digits_to_bits_multiple_digits(self):
        self.assertEqual(
            self.calc.digits_to_bits([1, 2, 3]),
            [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1]
        )

    def test_digits_to_bits_invalid_digit(self):
        with self.assertRaises(BCD2421Error):
            self.calc.digits_to_bits([10])
        with self.assertRaises(BCD2421Error):
            self.calc.digits_to_bits([-1])

    def test_bits_to_digits_single_digit(self):
        self.assertEqual(self.calc.bits_to_digits([0, 0, 0, 0]), [0])
        self.assertEqual(self.calc.bits_to_digits([1, 1, 1, 0]), [8])
        self.assertEqual(self.calc.bits_to_digits([1, 0, 1, 1]), [5])

    def test_bits_to_digits_multiple_digits(self):
        bits = [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 1, 1]  
        self.assertEqual(self.calc.bits_to_digits(bits), [1, 2, 5])

    def test_bits_to_digits_invalid_length(self):
        with self.assertRaises(BCD2421Error):
            self.calc.bits_to_digits([0, 0, 0]) 

    def test_bits_to_digits_invalid_pattern(self):
        
        with self.assertRaises(BCD2421Error):
            self.calc.bits_to_digits([0,1,1,0]) 
            
    def test_add_single_digit_no_carry(self):
        a_bits = self.calc.digits_to_bits([3])
        b_bits = self.calc.digits_to_bits([4])
        sum_bits, carry = self.calc.add_single_digit(a_bits, b_bits, 0)
        self.assertEqual(self.calc.bits_to_digits(sum_bits), [7])
        self.assertEqual(carry, 0)

    def test_add_single_digit_with_carry(self):
        a_bits = self.calc.digits_to_bits([7])
        b_bits = self.calc.digits_to_bits([5])
        sum_bits, carry = self.calc.add_single_digit(a_bits, b_bits, 0)
        self.assertEqual(self.calc.bits_to_digits(sum_bits), [2])
        self.assertEqual(carry, 1)

    def test_add_numbers_no_carry(self):
        a = [1, 2]  
        b = [2, 3] 
        result_bits, result_digits = self.calc.add_numbers(a, b)
        self.assertEqual(result_digits, [3, 5])  

    def test_add_numbers_with_carry(self):
        a = [2, 5]  
        b = [1, 6]  
        result_bits, result_digits = self.calc.add_numbers(a, b)
        self.assertEqual(result_digits, [4, 1]) 

    def test_add_numbers_diff_length(self):
        a = [1, 2]  
        b = [9]    
        result_bits, result_digits = self.calc.add_numbers(a, b)
        self.assertEqual(result_digits, [2, 1]) 
    def test_add_numbers_carry_overflow(self):
        a = [9, 9]  
        b = [1]    
        result_bits, result_digits = self.calc.add_numbers(a, b)
        self.assertEqual(result_digits, [1, 0, 0]) 
