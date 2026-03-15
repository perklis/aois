import unittest

from Minimization import Minimization
from src.ExpressionProperties import ExpressionProperties
from src.TruthTableBuilder import TruthTableBuilder


class TestMinimization(unittest.TestCase):
    def setUp(self):
        self.expression_service = ExpressionProperties()
        self.truth_service = TruthTableBuilder()
        self.min_service = Minimization()

    def _rows(self, expression):
        definition = self.expression_service.set_expression(expression)
        return self.truth_service.build(definition), definition.variables

    def test_calculation_method(self):
        rows, variables = self._rows("(!a&b&c)|(a&!b&!c)|(a&!b&c)|(a&b&!c)|(a&b&c)")
        result = self.min_service.minimize_calculation(rows, variables)
        self.assertIn("expression", result)
        self.assertTrue(result["selected"])

    def test_tabular_method_chart(self):
        rows, variables = self._rows("a|b")
        result = self.min_service.minimize_tabular(rows, variables)
        self.assertIn("chart", result)
        self.assertEqual(result["chart"]["minterms"], (1, 2, 3))

    def test_karnaugh_method(self):
        rows, variables = self._rows("a|b")
        result = self.min_service.minimize_karno(rows, variables)
        self.assertIn("map", result)
        self.assertIn("expression", result)

    def test_minimization_for_zero_function(self):
        rows, variables = self._rows("a&!a")
        result = self.min_service.minimize_calculation(rows, variables)
        self.assertEqual(result["expression"], "0")

    def test_minimize_both_calculation(self):
        rows, variables = self._rows("a|b")
        result = self.min_service.minimize_both(rows, variables, method="calculation")
        self.assertIn("sdnf", result)
        self.assertIn("sknf", result)
        self.assertIn("Минимизированная СДНФ", result["sdnf"]["result_label"])
        self.assertIn("Минимизированная СКНФ", result["sknf"]["result_label"])

    def test_minimize_sknf_for_or(self):
        rows, variables = self._rows("a|b")
        result = self.min_service.minimize_sknf(rows, variables, method="calculation")
        self.assertEqual(result["expression"], "(a | b)")
        self.assertEqual(result["form"], "sknf")

    def test_minimize_sknf_for_and(self):
        rows, variables = self._rows("a&b")
        result = self.min_service.minimize_sknf(rows, variables, method="calculation")
        self.assertIn("a", result["expression"])
        self.assertIn("b", result["expression"])

    def test_minimize_sknf_tabular_has_forms(self):
        rows, variables = self._rows("a|b")
        result = self.min_service.minimize_sknf(rows, variables, method="tabular")
        self.assertIn("column_forms", result)
        self.assertIn("row_forms", result)

    def test_minimize_sknf_karno_has_groups(self):
        rows, variables = self._rows("a|b")
        result = self.min_service.minimize_sknf(rows, variables, method="karno")
        self.assertIn("group_forms", result)

    def test_to_cnf_all_x_returns_zero(self):
        from models.Implicant import Implicant

        result = self.min_service._to_cnf((Implicant("--", [0]),), ("a", "b"))
        self.assertEqual(result, "0")


if __name__ == "__main__":
    unittest.main()
