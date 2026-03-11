import unittest

from parser.ExpressionParser import ExpressionParser
from parser.ToListOfTokens import ToListOfTokens


class TestParserTokenizer(unittest.TestCase):
    def setUp(self):
        self.tokenizer = ToListOfTokens()
        self.parser = ExpressionParser()

    def test_tokenize_simple_expression(self):
        tokens = self.tokenizer.tokenize("a&!b")
        values = [token.value for token in tokens]
        self.assertEqual(values, ["a", "&", "!", "b"])

    def test_tokenize_unicode_expression_error(self):
        with self.assertRaises(ValueError):
            self.tokenizer.tokenize("\u00ac(a\u2228b)")

    def test_tokenize_empty_expression_error(self):
        with self.assertRaises(ValueError):
            self.tokenizer.tokenize("   ")

    def test_tokenize_invalid_symbol_error(self):
        with self.assertRaises(ValueError):
            self.tokenizer.tokenize("a+b")

    def test_tokenize_reject_new_syntax(self):
        with self.assertRaises(ValueError):
            self.tokenizer.tokenize("a/\\b")

    def test_parse_and_evaluate(self):
        root = self.parser.parse(self.tokenizer.tokenize("(a|b)&!c"))
        value = root.evaluate({"a": 0, "b": 1, "c": 0})
        self.assertEqual(value, 1)

    def test_parse_implication_right_associative(self):
        root = self.parser.parse(self.tokenizer.tokenize("a->b->c"))
        value = root.evaluate({"a": 1, "b": 1, "c": 0})
        self.assertEqual(value, 0)

    def test_parse_equivalence(self):
        root = self.parser.parse(self.tokenizer.tokenize("a~b"))
        self.assertEqual(root.evaluate({"a": 1, "b": 1}), 1)
        self.assertEqual(root.evaluate({"a": 1, "b": 0}), 0)

    def test_parse_missing_parenthesis(self):
        with self.assertRaises(ValueError):
            self.parser.parse(self.tokenizer.tokenize("(a|b"))


if __name__ == "__main__":
    unittest.main()
