import unittest
from IEEENumbers import IEEENumber 

class TestIEEENumber(unittest.TestCase):

    def test_constructor_default_and_custom_bits(self):
        n1 = IEEENumber()
        self.assertEqual(len(n1.bits), 32)
        self.assertTrue(all(b == 0 for b in n1.bits))

        bits = [1]*32
        n2 = IEEENumber(bits)
        self.assertEqual(n2.bits, bits)
        bits[0] = 0
        self.assertNotEqual(n2.bits[0], bits[0])

    def test_copy(self):
        n = IEEENumber([1]+[0]*31)
        n_copy = n.copy()
        self.assertEqual(n.bits, n_copy.bits)
        
        n.bits[1] = 1
        self.assertNotEqual(n.bits, n_copy.bits)

    def test_getters_and_bits_str(self):
        bits = [1] + [0,1,0,1,0,1,0,1] + [1]*23
        n = IEEENumber(bits)
        self.assertEqual(n.get_sign(), 1)
        self.assertEqual(n.get_exponent_bits(), [0,1,0,1,0,1,0,1])
        self.assertEqual(n.get_mantissa_bits(), [1]*23)
        self.assertEqual(n.get_bits_str(), ''.join(str(b) for b in bits))

    def test_print_in_ieee_format_runs(self):
        bits = [1]+[0]*8+[1]*23
        n = IEEENumber(bits)
        n.print_in_ieee_format() 

    def test_from_bits_to_decimal(self):
   
        n = IEEENumber([0]*32)
        self.assertEqual(n.from_bits_to_decimal(), 0.0)

        n = IEEENumber([1]+[0]*31)
        self.assertEqual(n.from_bits_to_decimal(), -0.0)

        n = IEEENumber([0]+[1]*8+[0]*23)
        self.assertEqual(n.from_bits_to_decimal(), float('inf'))

        n = IEEENumber([1]+[1]*8+[0]*23)
        self.assertEqual(n.from_bits_to_decimal(), float('-inf'))

        n = IEEENumber([0]+[1]*8+[0]*22+[1])
        self.assertNotEqual(n.from_bits_to_decimal(), n.from_bits_to_decimal())
   
        n = IEEENumber([0]+[0,1,1,1,1,1,1,1]+[0]*23)
        self.assertAlmostEqual(n.from_bits_to_decimal(), 1.0)

        bits = [1]+[1,0,0,0,0,0,0,0]+[0,1]+[0]*21
        n = IEEENumber(bits)
        self.assertAlmostEqual(n.from_bits_to_decimal(), -2.5)

        bits = [0]+[0]*8+[1]+[0]*22
        n = IEEENumber(bits)
        expected = 0.5 * (2**(1-127))
        self.assertAlmostEqual(n.from_bits_to_decimal(), expected)
