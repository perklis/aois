from tree_nodes.AstNode import AstNode
from constants import SYMBOL_AND, SYMBOL_EQUIVALENT, SYMBOL_IMPLIES, SYMBOL_OR


class BinaryNode(AstNode):
    def __init__(self, operator, left, right):
        self.operator = operator
        self.left = left
        self.right = right

    def evaluate(self, context):
        left_value = self.left.evaluate(context)
        right_value = self.right.evaluate(context)
        if self.operator == SYMBOL_AND:
            return left_value & right_value
        if self.operator == SYMBOL_OR:
            return left_value | right_value
        if self.operator == SYMBOL_IMPLIES:
            return (1 - left_value) | right_value
        if self.operator == SYMBOL_EQUIVALENT:
            return int(left_value == right_value)
        raise ValueError("Неизвестная операция")

    def variables(self):
        return self.left.variables().union(self.right.variables())
