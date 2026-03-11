class AstNode:
    def evaluate(self, context):
        raise NotImplementedError

    def variables(self):
        raise NotImplementedError
