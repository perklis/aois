import unittest

from BitUtils import assignment_to_index, bit_mask_for_variable, index_to_assignment
from models.FunctionDefinition import FunctionDefinition
from models.Implicant import Implicant
from models.TruthTableRow import TruthTableRow


class TestUtilsModels(unittest.TestCase):
    def test_bit_utils(self):
        names = ("a", "b", "c")
        assignment = index_to_assignment(5, names)
        self.assertEqual(assignment, {"a": 1, "b": 0, "c": 1})
        self.assertEqual(assignment_to_index(assignment, names), 5)
        self.assertEqual(bit_mask_for_variable("b", names), 2)

    def test_models(self):
        row = TruthTableRow(1, {"a": 0}, 1)
        self.assertEqual(row.index, 1)
        self.assertEqual(row.value, 1)
        implicant = Implicant("1-", [2, 3])
        self.assertEqual(implicant.minterms, (2, 3))
        self.assertEqual(implicant.key(), "1-")
        function = FunctionDefinition("a", object(), ("a",))
        self.assertEqual(function.source, "a")


if __name__ == "__main__":
    unittest.main()
