import unittest

from lab4.KeyValueCalculator import KeyValueCalculator


class TestKeyToValue(unittest.TestCase):
    def test_ru_mapping(self):
        calc = KeyValueCalculator()
        self.assertEqual(calc.key_to_value("Вя"), 2 * 33 + 32)

    def test_en_mapping_case_insensitive(self):
        calc = KeyValueCalculator()
        self.assertEqual(calc.key_to_value("bA"), 26)

    def test_single_letter_key(self):
        calc = KeyValueCalculator()
        self.assertEqual(calc.key_to_value("C"), 2 * 26 + 2)

    def test_mixed_alphabet_raises(self):
        calc = KeyValueCalculator()
        with self.assertRaises(ValueError):
            calc.key_to_value("Aя")

    def test_empty_key_raises(self):
        calc = KeyValueCalculator()
        with self.assertRaises(ValueError):
            calc.key_to_value("   ")

    def test_non_string_key_raises(self):
        calc = KeyValueCalculator()
        with self.assertRaises(TypeError):
            calc.key_to_value(123)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
