from BitUtils import bit_mask_for_variable


class IsFictiveVariable:
    def find(self, rows, variable_names):
        values = tuple(row.value for row in rows)
        result = []
        for variable in variable_names:
            if self._is_fictive(variable, values, variable_names):
                result.append(variable)
        return tuple(result)

    def _is_fictive(self, variable, values, variable_names):
        mask = bit_mask_for_variable(variable, variable_names)
        for index in range(len(values)):
            if index & mask:
                continue
            if values[index] != values[index | mask]:
                return False
        return True
