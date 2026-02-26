import unittest
from exceptions import BCD2421Error
from BCD2421Calculator import BCD2421Calculator

class TestBCD2421Calculator(unittest.TestCase):

    def setUp(self):
        self.calc = BCD2421Calculator()

    def test_digits_to_bits_and_back(self):
        digits = [1, 2, 3, 4, 5, 0, 9]
        bits = self.calc.digits_to_bits(digits)
        restored = self.calc.bits_to_digits(bits)
        self.assertEqual(digits, restored, "Преобразование digits -> bits -> digits не совпадает")

    def test_single_digit_addition_no_carry(self):
        a_bits = self.calc.digits_to_bits([2])[0:4]
        b_bits = self.calc.digits_to_bits([3])[0:4]
        result_bits, carry = self.calc.add_single_digit(a_bits, b_bits, 0)
        result_digit = self.calc.bits_to_digits(result_bits)
        self.assertEqual(result_digit, [5])
        self.assertEqual(carry, 0)

    def test_single_digit_addition_with_carry(self):
        a_bits = self.calc.digits_to_bits([7])[0:4]
        b_bits = self.calc.digits_to_bits([5])[0:4]
        result_bits, carry = self.calc.add_single_digit(a_bits, b_bits, 0)
        result_digit = self.calc.bits_to_digits(result_bits)
        self.assertEqual(result_digit, [2])
        self.assertEqual(carry, 1)

    def test_add_numbers_no_carry(self):
        a = self.calc.digits_to_bits([1, 2])
        b = self.calc.digits_to_bits([3, 4])
        result = self.calc.add_numbers(a, b)
        result_digits = self.calc.bits_to_digits(result)
        self.assertEqual(result_digits, [4, 6])

    def test_add_numbers_with_carry(self):
        a = self.calc.digits_to_bits([9, 8])
        b = self.calc.digits_to_bits([3, 5])
        result = self.calc.add_numbers(a, b)
        result_digits = self.calc.bits_to_digits(result)
        self.assertEqual(result_digits, [1, 3, 3])

    def test_invalid_digit_raises_error(self):
        with self.assertRaises(BCD2421Error):
            self.calc.digits_to_bits([10])

    def test_invalid_bits_length_raises_error(self):
        with self.assertRaises(BCD2421Error):
            self.calc.bits_to_digits([0, 1, 0])  

    def test_bits_to_digits_invalid_chunk_raises_error(self):
        invalid_bits = [0, 0, 0, 0, 1, 1, 1, 0]  
        with self.assertRaises(BCD2421Error):
            self.calc.bits_to_digits(invalid_bits)

    def test_add_numbers_length_mismatch_raises_error(self):
        a = self.calc.digits_to_bits([1, 2])
        b = self.calc.digits_to_bits([3])
        with self.assertRaises(BCD2421Error):
            self.calc.add_numbers(a, b)
