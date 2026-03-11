import unittest

from services.SdnfSknfBuilder import SdnfSknfBuilder
from services.Differentiation import Differentiation
from services.ExpressionProperties import ExpressionProperties
from services.FictiveVariableService import IsFictiveVariable
from services.PostClassService import PostClassService
from services.TruthTableBuilder import TruthTableBuilder
from services.ZhegalkinPolinom import ZhegalkinPolinom


class TestServices(unittest.TestCase):
    def setUp(self):
        self.expression_service = ExpressionProperties()
        self.truth_service = TruthTableBuilder()
        self.canonical_service = SdnfSknfBuilder()
        self.post_service = PostClassService()
        self.zhegalkin_service = ZhegalkinPolinom()
        self.fictive_service = IsFictiveVariable()
        self.derivative_service = Differentiation()

    def test_expression_shape_flags(self):
        self.expression_service.set_expression("!(!a->!b)|c")
        shape = self.expression_service.analyze_shape()
        self.assertTrue(shape["has_single_negation"])
        self.assertTrue(shape["has_group_negation"])

    def test_truth_table_size(self):
        definition = self.expression_service.set_expression("a|b|c")
        rows = self.truth_service.build(definition)
        self.assertEqual(len(rows), 8)

    def test_canonical_forms(self):
        definition = self.expression_service.set_expression("a|b")
        rows = self.truth_service.build(definition)
        info = self.canonical_service.build(rows, definition.variables)
        self.assertEqual(info["ones"], (1, 2, 3))
        self.assertEqual(info["zeros"], (0,))
        self.assertEqual(info["index_decimal"], 7)

    def test_post_classes(self):
        definition = self.expression_service.set_expression("a|b")
        rows = self.truth_service.build(definition)
        info = self.post_service.analyze(rows, definition.variables)
        self.assertTrue(info["T0"])
        self.assertTrue(info["T1"])

    def test_zhegalkin_polynomial(self):
        definition = self.expression_service.set_expression("a~b")
        rows = self.truth_service.build(definition)
        polynomial = self.zhegalkin_service.build(rows, definition.variables)
        self.assertIsInstance(polynomial, str)

    def test_fictive_variable_found(self):
        definition = self.expression_service.set_expression("(a&b)|(a&!b)")
        rows = self.truth_service.build(definition)
        fictive = self.fictive_service.find(rows, definition.variables)
        self.assertEqual(fictive, ("b",))

    def test_derivative_partial(self):
        definition = self.expression_service.set_expression("a&b")
        rows = self.truth_service.build(definition)
        result = self.derivative_service.build(rows, definition.variables, ("a",))
        self.assertEqual(result["vector"], (0, 1, 0, 1))

    def test_derivative_validation(self):
        definition = self.expression_service.set_expression("a&b")
        rows = self.truth_service.build(definition)
        with self.assertRaises(ValueError):
            self.derivative_service.build(rows, definition.variables, tuple())


if __name__ == "__main__":
    unittest.main()
