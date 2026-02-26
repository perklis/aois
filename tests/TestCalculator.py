import unittest
from NumbersConverter import NumbersConverter, FRAC_BITS
from Calculator import Calculator

class TestCalculator(unittest.TestCase):

    def setUp(self):
        self.calc = Calculator()

    def test_add_positive(self):
        a = NumbersConverter.from_decimal_to_direct_code(5)
        b = NumbersConverter.from_decimal_to_direct_code(3)
        result = self.calc.add(a, b)
        self.assertEqual(result.from_direct_code_to_decimal(), 8)

    def test_add_negative(self):
        a = NumbersConverter.from_decimal_to_direct_code(-5)
        b = NumbersConverter.from_decimal_to_direct_code(3)
        result = self.calc.add(a, b)
        self.assertEqual(result.from_direct_code_to_decimal(), -2)

    def test_negate(self):
        a = NumbersConverter.from_decimal_to_direct_code(7)
        result = self.calc.negate(a)
        self.assertEqual(result.from_direct_code_to_decimal(), -7)

    def test_subtract(self):
        a = NumbersConverter.from_decimal_to_direct_code(17890)
        b = NumbersConverter.from_decimal_to_direct_code(890)
        result = self.calc.subtract(a, b)
        self.assertEqual(result.from_direct_code_to_decimal(), 17000)

    def test_multiply_positive(self):
        a = NumbersConverter.from_decimal_to_direct_code(6)
        b = NumbersConverter.from_decimal_to_direct_code(3)
        result = self.calc.multiply(a, b)
        self.assertEqual(result.from_direct_code_to_decimal(), 18)

    def test_multiply_negative(self):
        a = NumbersConverter.from_decimal_to_direct_code(-400)
        b = NumbersConverter.from_decimal_to_direct_code(3)
        result = self.calc.multiply(a, b)
        self.assertEqual(result.from_direct_code_to_decimal(), -1200)

    def test_divide_integer(self):
        a = NumbersConverter.from_decimal_to_direct_code(20)
        b = NumbersConverter.from_decimal_to_direct_code(5)
        result = self.calc.divide(a, b)
        self.assertEqual(result.to_decimal_division(), 4)

    def test_divide_fraction(self):
        a = NumbersConverter.from_decimal_to_direct_code(10)
        b = NumbersConverter.from_decimal_to_direct_code(3)
        result = self.calc.divide(a, b)

        expected = int((10 / 3) * (2 ** FRAC_BITS)) / (2 ** FRAC_BITS)
        self.assertAlmostEqual(result.to_decimal_division(), expected)

    def test_divide_by_zero(self):
        a = NumbersConverter.from_decimal_to_direct_code(10)
        b = NumbersConverter.from_decimal_to_direct_code(0)
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(a, b)

    def test_add_direct(self):
        a = [0]*31 + [1]
        b = [0]*31 + [1]
        result = self.calc.add_direct(a, b)
        self.assertEqual(result[-1], 0) 
        self.assertEqual(result[-2], 1) 

    def test_is_zero_true(self):
        zero = NumbersConverter.from_decimal_to_direct_code(0)
        self.assertTrue(self.calc.is_zero(zero.bits))

    def test_is_zero_false(self):
        num = NumbersConverter.from_decimal_to_direct_code(1)
        self.assertFalse(self.calc.is_zero(num.bits))