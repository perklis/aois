import unittest
from exceptions import InvalidDecimalInputError
from NumbersConverter import NumbersConverter, SCALE


class TestNumbersConverter(unittest.TestCase):
    def test_from_decimal_to_direct_code_positive(self):
        n = NumbersConverter.from_decimal_to_direct_code(10)
        self.assertEqual(n.from_direct_code_to_decimal(), 10)
        self.assertEqual(n.get_direct_code()[0], 0)

    def test_from_decimal_to_direct_code_negative(self):
        n = NumbersConverter.from_decimal_to_direct_code(-10)
        self.assertEqual(n.from_direct_code_to_decimal(), -10)
        self.assertEqual(n.get_direct_code()[0], 1)

    def test_from_decimal_to_direct_code_zero(self):
        n = NumbersConverter.from_decimal_to_direct_code(0)
        self.assertEqual(n.from_direct_code_to_decimal(), 0)
        self.assertEqual(n.get_direct_code()[0], 0)

    def test_from_decimal_to_direct_code_invalid_input(self):
        with self.assertRaises(InvalidDecimalInputError):
            NumbersConverter.from_decimal_to_direct_code(3.14)
        with self.assertRaises(InvalidDecimalInputError):
            NumbersConverter.from_decimal_to_direct_code("123")

    def test_get_ones_complement_positive(self):
        n = NumbersConverter.from_decimal_to_direct_code(10)
        ones = n.get_ones_complement()
        self.assertEqual(ones[0], 0)
        self.assertEqual(ones,n.get_direct_code())

    def test_get_ones_complement_negative(self):
        n = NumbersConverter.from_decimal_to_direct_code(-5)
        ones = n.get_ones_complement()
        self.assertEqual(ones[0], 1)
        self.assertNotEqual(ones[1:], n.get_direct_code()[1:])

    def test_get_twos_complement_positive(self):
        n = NumbersConverter.from_decimal_to_direct_code(5)
        twos = n.get_twos_complement()
        self.assertEqual(twos, n.get_direct_code())

    def test_get_twos_complement_negative(self):
        n = NumbersConverter.from_decimal_to_direct_code(-1)
        twos = n.get_twos_complement()
        self.assertNotEqual(twos, n.get_direct_code())

    def test_from_twos_to_direct_positive(self):
        n = NumbersConverter.from_twos_to_direct([0] + [0] * 31)
        self.assertEqual(n.from_direct_code_to_decimal(), 0)

        bits = NumbersConverter.from_decimal_to_direct_code(-5).get_twos_complement()
        n = NumbersConverter.from_twos_to_direct(bits)
        self.assertEqual(n.from_direct_code_to_decimal(), -5)

    def test_to_decimal_scaled(self):
        n = NumbersConverter.from_decimal_to_direct_code(10)
        self.assertEqual(n.to_decimal_scaled(), 10 / SCALE)

    def test_str_method(self):
        n = NumbersConverter.from_decimal_to_direct_code(-5)
        s = str(n)
        self.assertIn("Десятичное", s)
        self.assertIn("Прямой код", s)
        self.assertIn("Обратный код", s)
        self.assertIn("Дополнительный код", s)
