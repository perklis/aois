import unittest
from IEEECalculator import IEEECalculator

class TestIEEECalculator(unittest.TestCase):
    def setUp(self):
        self.calc = IEEECalculator()

    def test_extract_sign(self):
        sign, num = self.calc._extract_sign("-12.5")
        self.assertEqual(sign, 1)
        self.assertEqual(num, "12.5")

        sign, num = self.calc._extract_sign("12.5")
        self.assertEqual(sign, 0)

    def test_split_parts(self):
        i, f = self.calc._split_parts("12.75")
        self.assertEqual(i, "12")
        self.assertEqual(f, "75")

        i, f = self.calc._split_parts("15")
        self.assertEqual(f, "0")

    def test_is_zero(self):
        self.assertTrue(self.calc._is_zero("0", "0"))
        self.assertTrue(self.calc._is_zero("000", "000"))
        self.assertFalse(self.calc._is_zero("1", "0"))

    def test_convert_integer_part(self):
        self.assertEqual(self.calc._from_int_part_to_bits("5"), [1, 0, 1])
        self.assertEqual(self.calc._from_int_part_to_bits("0"), [0])

    def test_convert_fraction_part(self):
        bits = self.calc._fraction_part_to_bits("5")
        self.assertEqual(bits[0], 1)

    def test_decimal_to_ieee_zero(self):
        num = self.calc.decimal_to_ieee("0")
        self.assertTrue(self.calc.is_zero(num))

    def test_decimal_to_ieee_positive(self):
        num = self.calc.decimal_to_ieee("2")
        self.assertEqual(num.get_sign(), 0)

    def test_decimal_to_ieee_negative(self):
        num = self.calc.decimal_to_ieee("-2")
        self.assertEqual(num.get_sign(), 1)

    def test_add_simple(self):
        a = self.calc.decimal_to_ieee("2")
        b = self.calc.decimal_to_ieee("2")
        result = self.calc.add(a, b)
        self.assertEqual(result.get_sign(), 0)

    def test_add_opposite_numbers(self):
        a = self.calc.decimal_to_ieee("2")
        b = self.calc.decimal_to_ieee("-2")
        result = self.calc.add(a, b)
        self.assertTrue(self.calc.is_zero(result))

    def test_add_with_zero(self):
        a = self.calc.decimal_to_ieee("0")
        b = self.calc.decimal_to_ieee("5")
        result = self.calc.add(a, b)
        self.assertEqual(result.get_sign(), 0)

    def test_subtract(self):
        a = self.calc.decimal_to_ieee("5")
        b = self.calc.decimal_to_ieee("3")
        result = self.calc.subtract(a, b)
        self.assertEqual(result.get_sign(), 0)

    def test_multiply_simple(self):
        a = self.calc.decimal_to_ieee("2")
        b = self.calc.decimal_to_ieee("3")
        result = self.calc.multiply(a, b)
        self.assertEqual(result.get_sign(), 0)

    def test_multiply_negative(self):
        a = self.calc.decimal_to_ieee("-2")
        b = self.calc.decimal_to_ieee("3")
        result = self.calc.multiply(a, b)
        self.assertEqual(result.get_sign(), 1)

    def test_multiply_zero(self):
        a = self.calc.decimal_to_ieee("0")
        b = self.calc.decimal_to_ieee("5")
        result = self.calc.multiply(a, b)
        self.assertTrue(self.calc.is_zero(result))

    def test_divide_simple(self):
        a = self.calc.decimal_to_ieee("6")
        b = self.calc.decimal_to_ieee("2")
        result = self.calc.divide(a, b)
        self.assertEqual(result.get_sign(), 0)

    def test_divide_negative(self):
        a = self.calc.decimal_to_ieee("-6")
        b = self.calc.decimal_to_ieee("2")
        result = self.calc.divide(a, b)
        self.assertEqual(result.get_sign(), 1)

    def test_divide_by_zero_returns_infinity(self):
        a = self.calc.decimal_to_ieee("6")
        b = self.calc.decimal_to_ieee("0")

        result = self.calc.divide(a, b)

        self.assertTrue(self.calc.is_infinity(result))
        self.assertEqual(result.get_sign(), 0)

    def test_divide_negative_by_zero_returns_negative_infinity(self):
        a = self.calc.decimal_to_ieee("-6")
        b = self.calc.decimal_to_ieee("0")

        result = self.calc.divide(a, b)

        self.assertTrue(self.calc.is_infinity(result))
        self.assertEqual(result.get_sign(), 1)

    def test_zero_div_zero_returns_nan(self):
        a = self.calc.decimal_to_ieee("0")
        b = self.calc.decimal_to_ieee("0")

        result = self.calc.divide(a, b)

        self.assertTrue(self.calc.is_nan(result))
