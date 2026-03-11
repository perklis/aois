from tree_nodes.AstNode import AstNode


class VariableNode(AstNode):
    def __init__(self, name):
        self.name = name

    def evaluate(self, context):
        return context[self.name]

    def variables(self):
        return {self.name}
