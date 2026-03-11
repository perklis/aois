from tree_nodes.AstNode import AstNode


class UnaryNode(AstNode):
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def evaluate(self, context):
        return 1 - self.operand.evaluate(context)

    def variables(self):
        return self.operand.variables()
