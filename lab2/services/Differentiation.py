from BitUtils import bit_mask_for_variable
from constants import SYMBOL_AND, SYMBOL_OR, MAX_DERIVATIVE_ORDER


class Differentiation:
    """Частные и смешанные производные по списку переменных."""

    def build(self, rows, variable_names, variables):
        self._validate(variables, variable_names)
        values = [row.value for row in rows]
        for variable in variables:
            mask = bit_mask_for_variable(variable, variable_names)
            values = self._single(values, mask)
        return {
            "variables": tuple(variables),
            "vector": tuple(values),
            "sdnf": self._sdnf(values, variable_names),
        }

    def _validate(self, variables, variable_names):
        if not variables:
            raise ValueError("Нужно указать хотя бы одну переменную")
        if len(variables) > MAX_DERIVATIVE_ORDER:
            raise ValueError("Порядок производной должен быть от 1 до 4")
        for variable in variables:
            if variable not in variable_names:
                raise ValueError(f"Переменная {variable} не используется")

    def _single(self, values, mask):
        result = []
        for index in range(len(values)):
            result.append(values[index] ^ values[index ^ mask])
        return result

    def _sdnf(self, values, variable_names):
        ones = [index for index, value in enumerate(values) if value == 1]
        if not ones:
            return "0"
        terms = []
        width = len(variable_names)
        for index in ones:
            literals = []
            for offset, name in enumerate(variable_names):
                bit = (index >> (width - 1 - offset)) & 1
                literals.append(name if bit == 1 else f"!{name}")
            terms.append("(" + f" {SYMBOL_AND} ".join(literals) + ")")
        return f" {SYMBOL_OR} ".join(terms)
