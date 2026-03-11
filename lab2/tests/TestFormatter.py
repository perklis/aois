import unittest

from services.FunctionAnalyzator import FunctionAnalyzator
from ResultFormatter import ResultFormatter


class TestFormatter(unittest.TestCase):
    def setUp(self):
        self.facade = FunctionAnalyzator()
        self.formatter = ResultFormatter()

    def test_facade_pipeline(self):
        self.facade.set_expression("a|b")
        shape = self.facade.shape()
        table = self.facade.truth_table()
        canonical = self.facade.canonical()
        post = self.facade.post()
        zhegalkin = self.facade.zhegalkin()
        fictive = self.facade.fictive()
        self.assertEqual(shape["count"], 2)
        self.assertEqual(len(table), 4)
        self.assertIn("sdnf", canonical)
        self.assertIn("T0", post)
        self.assertIsInstance(zhegalkin, str)
        self.assertEqual(fictive, tuple())

    def test_formatter_outputs(self):
        self.facade.set_expression("a|b")
        definition = self.facade.definition()
        table = self.facade.truth_table()
        shape_text = self.formatter.shape_text(self.facade.shape())
        table_text = self.formatter.truth_table_text(table, definition.variables)
        canonical_text = self.formatter.canonical_text(self.facade.canonical())
        post_text = self.formatter.post_text(self.facade.post())
        derivative_text = self.formatter.derivative_text(self.facade.derivative(("a",)))
        min_text = self.formatter.minimization_text(self.facade.minimize_calculation())
        tab_text = self.formatter.tabular_chart_text(self.facade.minimize_tabular())
        kmap_text = self.formatter.karnaugh_text(self.facade.minimize_karnaugh())
        self.assertIn("Анализ", shape_text)
        self.assertIn("idx", table_text)
        self.assertIn("СДНФ", canonical_text)
        self.assertIn("T0", post_text)
        self.assertIn("Булева производная", derivative_text)
        self.assertIn("Минимизированная ДНФ", min_text)
        self.assertIn("implicant", tab_text)
        self.assertIn("row/col", kmap_text)
