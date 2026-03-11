from constants import (
    MAX_VARIABLES,
    SYMBOL_AND,
    SYMBOL_EQUIVALENT,
    SYMBOL_IMPLIES,
    SYMBOL_OPEN_BRACKET,
    SYMBOL_NOT,
    SYMBOL_OR,
    SYMBOL_CLOSE_BRACKET,
)
from tree_nodes.BinaryNode import BinaryNode
from tree_nodes.UnaryNode import UnaryNode
from tree_nodes.VariableNode import VariableNode


class ExpressionParser:
    def __init__(self):
        self.tokens = []
        self.index = 0

    def parse(self, tokens):
        self.tokens = tokens
        self.index = 0
        root = self._parse_equivalent()
        if self.index != len(self.tokens):
            raise ValueError("Лишние символы в конце")
        if len(root.variables()) > MAX_VARIABLES:
            raise ValueError("Превышено число переменных")
        return root

    def _parse_equivalent(self):
        node = self._parse_implication()
        while self._match_op(SYMBOL_EQUIVALENT):
            node = BinaryNode(SYMBOL_EQUIVALENT, node, self._parse_implication())
        return node

    def _parse_implication(self):
        node = self._parse_or()
        if self._match_op(SYMBOL_IMPLIES):
            return BinaryNode(SYMBOL_IMPLIES, node, self._parse_implication())
        return node

    def _parse_or(self):
        node = self._parse_and()
        while self._match_op(SYMBOL_OR):
            node = BinaryNode(SYMBOL_OR, node, self._parse_and())
        return node

    def _parse_and(self):
        node = self._parse_unary()
        while self._match_op(SYMBOL_AND):
            node = BinaryNode(SYMBOL_AND, node, self._parse_unary())
        return node

    def _parse_unary(self):
        if self._match_op(SYMBOL_NOT):
            return UnaryNode(SYMBOL_NOT, self._parse_unary())
        return self._parse_atom()

    def _parse_atom(self):
        token = self._peek()
        if token is None:
            raise ValueError("Неожиданный конец выражения")
        if token.token_type == "VAR":
            self.index += 1
            return VariableNode(token.value)
        if token.token_type == "PAR" and token.value == SYMBOL_OPEN_BRACKET:
            self.index += 1
            inner = self._parse_equivalent()
            self._expect_brackets(SYMBOL_CLOSE_BRACKET)
            return inner
        raise ValueError(f"Неожиданный токен: {token.value}")

    def _match_op(self, op_value):
        token = self._peek()
        if token is None:
            return False
        if token.token_type != "OP" or token.value != op_value:
            return False
        self.index += 1
        return True

    def _expect_brackets(self, paren_value):
        token = self._peek()
        if token is None:
            raise ValueError("Ожидалась скобка")
        if token.token_type == "PAR" and token.value == paren_value:
            self.index += 1
            return
        raise ValueError(f"Ожидалась скобка {paren_value}")

    def _peek(self):
        if self.index >= len(self.tokens):
            return None
        return self.tokens[self.index]
