from itertools import combinations
from constants import SYMBOL_AND, SYMBOL_OR
from models.Implicant import Implicant


class Minimization:
    def minimize_calculation(self, rows, variable_names):
        minterms = tuple(row.index for row in rows if row.value == 1)
        stages, prime = self._glue(minterms, len(variable_names))
        selected = self._remove_unnecessary(prime, minterms)
        return {
            "variable_names": variable_names,
            "stages": stages,
            "prime": prime,
            "selected": selected,
            "expression": self._to_expression(selected, variable_names),
        }

    def minimize_tabular(self, rows, variable_names):
        result = self.minimize_calculation(rows, variable_names)
        chart = self._build_chart(
            result["prime"], tuple(row.index for row in rows if row.value == 1)
        )
        selected = self._select_from_chart(chart)
        if selected:
            result["selected"] = selected
            result["expression"] = self._to_expression(selected, variable_names)
        result["chart"] = chart
        result["variable_names"] = variable_names
        return result

    def minimize_karno(self, rows, variable_names):
        result = self.minimize_tabular(rows, variable_names)
        kmap = self._build_karno_map(rows, variable_names)
        return {
            "variable_names": variable_names,
            "map": kmap,
            "groups": [item.pattern for item in result["selected"]],
            "expression": result["expression"],
        }

    def _glue(self, minterms, width):
        if not minterms:
            return [tuple()], tuple()
        current = tuple(
            Implicant(format(index, f"0{width}b"), [index]) for index in minterms
        )
        stages = []
        prime = []
        while True:
            combined, unused, glued = self._combine_once(current)
            stages.append({"implicants": current, "glued": glued})
            prime.extend(unused)
            if not combined:
                break
            current = combined
        return stages, self._deduplicate(prime)

    def _combine_once(self, implicants):
        used = set()
        combined = []
        glued = []
        for left in range(len(implicants)):
            for right in range(left + 1, len(implicants)):
                item = self._combine_pair(implicants[left], implicants[right])
                if item is None:
                    continue
                used.add(left)
                used.add(right)
                combined.append(item)
                glued.append((implicants[left], implicants[right], item))
        unused = [implicants[i] for i in range(len(implicants)) if i not in used]
        return self._deduplicate(combined), tuple(unused), glued

    def _combine_pair(self, left, right):
        diff = 0
        pattern = []
        for lbit, rbit in zip(left.pattern, right.pattern):
            if lbit == rbit:
                pattern.append(lbit)
                continue
            if "-" in (lbit, rbit):
                return None
            diff += 1
            pattern.append("-")
        if diff != 1:
            return None
        merged = sorted(set(left.minterms).union(right.minterms))
        return Implicant("".join(pattern), merged)

    def _remove_unnecessary(self, implicants, minterms):
        selected = list(implicants)
        for candidate in implicants:
            if candidate not in selected:
                continue
            others = [item for item in selected if item != candidate]
            if self._covers(others, minterms):
                selected = others
        return tuple(selected)

    def _covers(self, implicants, minterms):
        covered = set()
        for item in implicants:
            covered.update(item.minterms)
        for minterm in minterms:
            if minterm not in covered:
                return False
        return True

    def _to_expression(self, implicants, variable_names):
        if not implicants:
            return "0"
        terms = []
        for implicant in implicants:
            literals = []
            for name, symbol in zip(variable_names, implicant.pattern):
                if symbol == "-":
                    continue
                literals.append(name if symbol == "1" else f"!{name}")
            if not literals:
                terms.append("1")
            elif len(literals) == 1:
                terms.append(literals[0])
            else:
                terms.append("(" + f" {SYMBOL_AND} ".join(literals) + ")")
        return f" {SYMBOL_OR} ".join(terms)

    def _deduplicate(self, implicants):
        merged = {}
        for item in implicants:
            if item.pattern not in merged:
                merged[item.pattern] = set()
            merged[item.pattern].update(item.minterms)
        result = []
        for pattern, minterms in merged.items():
            result.append(Implicant(pattern, sorted(minterms)))
        return tuple(sorted(result, key=lambda item: item.pattern))

    def _build_chart(self, implicants, minterms):
        matrix = []
        for item in implicants:
            row = []
            for minterm in minterms:
                row.append(1 if minterm in item.minterms else 0)
            matrix.append(tuple(row))
        return {"minterms": minterms, "implicants": implicants, "matrix": tuple(matrix)}

    def _select_from_chart(self, chart):
        implicants = chart["implicants"]
        minterms = chart["minterms"]
        matrix = chart["matrix"]
        selected = []
        for col in range(len(minterms)):
            rows = [row for row in range(len(implicants)) if matrix[row][col] == 1]
            if len(rows) == 1:
                item = implicants[rows[0]]
                if item not in selected:
                    selected.append(item)
        if self._covers(selected, minterms):
            return tuple(selected)
        pool = [item for item in implicants if item not in selected]
        for size in range(1, len(pool) + 1):
            for group in combinations(pool, size):
                candidate = selected + list(group)
                if self._covers(candidate, minterms):
                    return tuple(candidate)
        return tuple(selected)

    def _build_karno_map(self, rows, variable_names):
        count = len(variable_names)
        row_bits = count // 2
        col_bits = count - row_bits
        row_labels = self._gray(row_bits)
        col_labels = self._gray(col_bits)
        values = tuple(row.value for row in rows)
        matrix = []
        for row_label in row_labels:
            line = []
            for col_label in col_labels:
                bits = row_label + col_label
                line.append(values[int(bits, 2)] if bits else values[0])
            matrix.append(tuple(line))
        return {"rows": row_labels, "cols": col_labels, "values": tuple(matrix)}

    def _gray(self, bits):
        if bits == 0:
            return ("",)
        labels = []
        for value in range(1 << bits):
            gray = value ^ (value >> 1)
            labels.append(format(gray, f"0{bits}b"))
        return tuple(labels)
