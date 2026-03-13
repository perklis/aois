class ZhegalkinPolinom:
    def build(self, rows, variable_names):
        coeffs = self._coefs_triangle(rows)
        polinom_parts = []
        for index, value in enumerate(coeffs):
            if value == 1:
                polinom_parts.append(self._mask_to_monom(index, variable_names))
        return " xor ".join(polinom_parts) if polinom_parts else "0"

    def max_degree(self, rows, variable_names):
        coeffs = self._coefs_triangle(rows)
        max_value = 0
        for mask, value in enumerate(coeffs):
            if value == 0:
                continue
            degree = self._degree(mask, len(variable_names))
            max_value = max(max_value, degree)
        return max_value

    def _coefs_triangle(self, rows):
        values = [row.value for row in rows]
        if not values:
            return []
        coeffs = [values[0]]
        while len(values) > 1:
            values = [
                values[index] ^ values[index + 1] for index in range(len(values) - 1)
            ]
            coeffs.append(values[0])
        return coeffs

    def _mask_to_monom(self, mask, variable_names):
        if mask == 0:
            return "1"
        factors = []
        count_of_variables = len(variable_names)
        for offset, name in enumerate(variable_names):
            shift = count_of_variables - 1 - offset
            if (mask >> shift) & 1:
                factors.append(name)
        return "*".join(factors)

    def _degree(self, mask, variable_count):
        degree = 0
        for shift in range(variable_count):
            if (mask >> shift) & 1:
                degree += 1
        return degree
