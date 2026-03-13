from BitUtils import bit_mask_for_variable, index_to_assignment
from Minimization import Minimization
from constants import SYMBOL_AND, SYMBOL_OR, MAX_DERIVATIVE_ORDER
from models.TruthTableRow import TruthTableRow


class Differentiation:
    def build(self, rows, variable_names, variables):
        self._validate(variables, variable_names)
        values = [row.value for row in rows]
        for variable in variables:
            mask = bit_mask_for_variable(variable, variable_names)
            values = self._single(values, mask)
        formula = self._sdnf(values, variable_names)
        simplified = self._simplified_sdnf(values, variable_names)
        return {
            "variables": tuple(variables),
            "vector": tuple(values),
            "sdnf": formula,
            "formula": formula,
            "simplified_sdnf": simplified,
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

    def _simplified_sdnf(self, values, variable_names):
        rows = []
        for index, value in enumerate(values):
            assignment = index_to_assignment(index, variable_names)
            rows.append(TruthTableRow(index, assignment, value))
        result = Minimization().minimize_calculation(tuple(rows), variable_names)
        return result["expression"]
