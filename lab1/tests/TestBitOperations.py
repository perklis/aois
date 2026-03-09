import unittest
from BitOperations import BitOperations


class TestBitOperations(unittest.TestCase):
    def setUp(self):
        self.bits = BitOperations()

    def test_int_to_bits(self):
        result = self.bits.int_to_bits(5, 4)
        self.assertEqual(result, [0, 1, 0, 1])

    def test_bits_to_int(self):
        result = self.bits.bits_to_int([0, 1, 0, 1])
        self.assertEqual(result, 5)

    def test_round_trip_conversion(self):
        number = 13
        bits = self.bits.int_to_bits(number, 8)
        restored = self.bits.bits_to_int(bits)
        self.assertEqual(restored, number)

    def test_add_without_carry(self):
        a = [0, 1, 0, 1]
        b = [0, 0, 1, 0]
        result, carry = self.bits.add_bits(a, b)
        self.assertEqual(result, [0, 1, 1, 1])
        self.assertEqual(carry, 0)

    def test_add_with_carry(self):
        a = [1, 1, 1, 1]
        b = [0, 0, 0, 1]
        result, carry = self.bits.add_bits(a, b)
        self.assertEqual(result, [0, 0, 0, 0])
        self.assertEqual(carry, 1)

    def test_subtract_bits(self):
        a = [0, 1, 1, 0]
        b = [0, 0, 1, 1]
        result = self.bits.subtract_bits(a, b)
        self.assertEqual(result, [0, 0, 1, 1])

    def test_compare_equal(self):
        a = [0, 1, 0, 1]
        b = [0, 1, 0, 1]
        self.assertEqual(self.bits.compare_register(a, b), 0)

    def test_compare_greater(self):
        a = [0, 1, 1, 0]
        b = [0, 1, 0, 1]
        self.assertEqual(self.bits.compare_register(a, b), 1)

    def test_compare_less(self):
        a = [0, 0, 1, 0]
        b = [0, 1, 0, 1]
        self.assertEqual(self.bits.compare_register(a, b), -1)

    def test_move_left(self):
        bits = [1, 0, 1, 1]
        self.bits.move_left(bits)
        self.assertEqual(bits, [0, 1, 1, 0])

    def test_move_right(self):
        bits = [1, 0, 1, 1]
        self.bits.move_right(bits)
        self.assertEqual(bits, [0, 1, 0, 1])

    def test_sub_register(self):
        a = [0, 1, 1, 0]
        b = [0, 0, 1, 1]
        result = self.bits.sub_register(a, b)
        self.assertEqual(result, [0, 0, 1, 1])
