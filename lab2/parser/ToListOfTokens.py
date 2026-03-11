from constants import (
    ALLOWED_VARIABLES,
    SYMBOL_AND,
    SYMBOL_EQUIVALENT,
    SYMBOL_IMPLIES,
    SYMBOL_OPEN_BRACKET,
    SYMBOL_NOT,
    SYMBOL_OR,
    SYMBOL_CLOSE_BRACKET,
)
from parser.Token import Token


class ToListOfTokens:
    def tokenize(self, expression):
        normalized = self._normalize(expression)
        return self._scan(normalized)

    def _normalize(self, expression):
        text = expression.replace(" ", "").replace("\t", "").replace("\n", "")
        return text

    def _scan(self, expression):
        tokens = []
        index = 0
        while index < len(expression):
            next_index = self._find_symbol(expression, index, tokens)
            if next_index is not None:
                index = next_index
                continue
            if expression[index].isalpha():
                tokens.append(self._find_word(expression, index))
                index += 1
                continue
            raise ValueError(f"Недопустимый символ: {expression[index]}")
        if not tokens:
            raise ValueError("Пустое выражение")
        return tokens

    def _find_symbol(self, expression, index, tokens):
        symbol = expression[index]
        if symbol == "-":
            return self._find_implication(expression, index, tokens)
        if symbol in (SYMBOL_NOT, SYMBOL_AND, SYMBOL_OR, SYMBOL_EQUIVALENT):
            tokens.append(Token("OP", symbol))
            return index + 1
        if symbol in (SYMBOL_OPEN_BRACKET, SYMBOL_CLOSE_BRACKET):
            tokens.append(Token("PAR", symbol))
            return index + 1
        return None

    def _find_implication(self, expression, index, tokens):
        if index + 1 < len(expression) and expression[index + 1] == ">":
            tokens.append(Token("OP", SYMBOL_IMPLIES))
            return index + 2
        raise ValueError("Символ '-' должен быть частью '->'")

    def _find_word(self, expression, index):
        symbol = expression[index].lower()
        if symbol in ALLOWED_VARIABLES:
            return Token("VAR", symbol)
        raise ValueError(f"Неизвестный идентификатор: {symbol}")
