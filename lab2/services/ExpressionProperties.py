from models.FunctionDefinition import FunctionDefinition
from parser.ExpressionParser import ExpressionParser
from parser.ToListOfTokens import ToListOfTokens


class ExpressionProperties:
    def __init__(self):
        self.tokenizer = ToListOfTokens()
        self.parser = ExpressionParser()
        self.current = None

    def set_expression(self, expression):
        tokens = self.tokenizer.tokenize(expression)
        root = self.parser.parse(tokens)
        variables = tuple(sorted(root.variables()))
        self.current = FunctionDefinition(expression, root, variables)
        return self.current

    def require_definition(self):
        if self.current is None:
            raise ValueError("Введите функцию")
        return self.current

    def analyze_shape(self):
        definition = self.require_definition()
        source = definition.source
        return {
            "source": definition.source,
            "variables": definition.variables,
            "count": len(definition.variables),
            "has_single_negation": self._has_single_negation(source),
            "has_group_negation": self._has_group_negation(source),
        }

    def _has_single_negation(self, text):
        normalized = text.replace(" ", "")
        for index, symbol in enumerate(normalized[:-1]):
            if symbol == "!" and normalized[index + 1].isalpha():
                return True
        return False

    def _has_group_negation(self, text):
        normalized = text.replace(" ", "")
        return "!(" in normalized
