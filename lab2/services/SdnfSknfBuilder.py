from constants import EMPTY_TEXT, ONE_TEXT, SYMBOL_AND, SYMBOL_OR, ZERO_TEXT


class SdnfSknfBuilder:
    def build(self, rows, variable_names):
        ones = tuple(row.index for row in rows if row.value == 1)
        zeros = tuple(row.index for row in rows if row.value == 0)
        sdnf = self._build_sdnf(ones, variable_names)
        sknf = self._build_sknf(zeros, variable_names)
        return {
            "sdnf": sdnf,
            "sknf": sknf,
            "ones": ones,
            "zeros": zeros,
            "numeric_sdnf": self._numeric("S", ones),
            "numeric_sknf": self._numeric("P", zeros),
            "index_binary": self._index_binary(rows),
            "index_decimal": self._index_decimal(rows),
            "sdnf_constituents_ok": ones
            == tuple(row.index for row in rows if row.value == 1),
            "sknf_constituents_ok": zeros
            == tuple(row.index for row in rows if row.value == 0),
        }

    def _build_sdnf(self, minterms, variable_names):
        if not minterms:
            return ZERO_TEXT
        terms = []
        for index in minterms:
            terms.append(self._minterm(index, variable_names))
        return f" {SYMBOL_OR} ".join(terms)

    def _build_sknf(self, maxterms, variable_names):
        if not maxterms:
            return ONE_TEXT
        terms = []
        for index in maxterms:
            terms.append(self._maxterm(index, variable_names))
        return f" {SYMBOL_AND} ".join(terms)

    def _minterm(self, index, variable_names):
        parts = []
        count = len(variable_names)
        for offset, name in enumerate(variable_names):
            bit = (index >> (count - 1 - offset)) & 1
            parts.append(name if bit == 1 else f"!{name}")
        return "(" + f" {SYMBOL_AND} ".join(parts) + ")"

    def _maxterm(self, index, variable_names):
        parts = []
        count = len(variable_names)
        for offset, name in enumerate(variable_names):
            bit = (index >> (count - 1 - offset)) & 1
            parts.append(name if bit == 0 else f"!{name}")
        return "(" + f" {SYMBOL_OR} ".join(parts) + ")"

    def _numeric(self, prefix, values):
        if not values:
            return f"{prefix}({EMPTY_TEXT})"
        return f"{prefix}({', '.join(str(v) for v in values)})"

    def _index_binary(self, rows):
        return "".join(str(row.value) for row in rows)

    def _index_decimal(self, rows):
        return int(self._index_binary(rows), 2)
