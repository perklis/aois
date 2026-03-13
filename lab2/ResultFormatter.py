class ResultFormatter:
    def shape_text(self, shape):
        lines = ["\n"]
        lines.append(f"- Выражение: {shape['source']}")
        lines.append(f"- Переменные: {', '.join(shape['variables'])}")
        lines.append(f"- Количество переменных: {shape['count']}")
        lines.append(f"- Одиночное отрицание: {shape['has_single_negation']}")
        lines.append(f"- Групповое отрицание: {shape['has_group_negation']}")
        return "\n".join(lines)

    def truth_table_text(self, rows, variable_names):
        headers = ["idx", *variable_names, "f"]
        table_rows = []
        for row in rows:
            values = [str(row.index)]
            values.extend(str(row.assignment[name]) for name in variable_names)
            values.append(str(row.value))
            table_rows.append(values)
        return self._format_table(headers, table_rows)

    def canonical_text(self, info):
        lines = ["Канонические формы:"]
        lines.append(f"- Числовая форма СДНФ: {info['numeric_sdnf']}")
        lines.append(f"- Числовая форма СКНФ: {info['numeric_sknf']}")
        lines.append(f"- Индексная форма (вектор): {info['index_binary']}")
        lines.append(f"- Индексная форма (число): {info['index_decimal']}")
        return "\n".join(lines)

    def post_text(self, info):
        return "\n".join([
            "Классы Поста:",
            f"- T0: {info['T0']}",
            f"- T1: {info['T1']}",
            f"- S: {info['S']}",
            f"- M: {info['M']}",
            f"- L: {info['L']}",
        ])

    def derivative_text(self, info):
        vec = "".join(str(v) for v in info["vector"])
        variables = ", ".join(info["variables"])
        return "\n".join([
            f"Булева производная по [{variables}]",
            f"- Вектор: {vec}",
            f"- СДНФ: {info['sdnf']}",
            f"- СДНФ (упрощенная): {info['simplified_sdnf']}",
        ])

    def minimization_text(self, info):
        lines = []
        variable_names = info["variable_names"]
        for index, stage in enumerate(info["stages"], start=1):
            forms = [
                self._pattern_to_form(item.pattern, variable_names)
                for item in stage["implicants"]
            ]
            lines.append(f"Этап {index} склеивания: " + ", ".join(forms))
            if stage["glued"]:
                lines.append("Склеенные импликанты:")
                for left, right, result in stage["glued"]:
                    left_form = self._pattern_to_form(left.pattern, variable_names)
                    right_form = self._pattern_to_form(right.pattern, variable_names)
                    result_form = self._pattern_to_form(result.pattern, variable_names)
                    lines.append(f"{left_form} + {right_form} -> {result_form}")
        lines.append("Простые импликанты: " + self._patterns(info["prime"], variable_names))
        lines.append("Выбранные импликанты: " + self._patterns(info["selected"], variable_names))
        lines.append("Минимизированная ДНФ: " + info["expression"])
        return "\n".join(lines)

    def tabular_chart_text(self, info):
        chart = info["chart"]
        if not chart["minterms"]:
            return "Таблица покрытия: нет минтермов"
        variable_names = info["variable_names"]
        minterm_forms = [
            self._minterm_form(value, variable_names) for value in chart["minterms"]
        ]
        headers = ["implicant", *minterm_forms]
        table_rows = []
        for implicant, row in zip(chart["implicants"], chart["matrix"]):
            marks = ["X" if value == 1 else "." for value in row]
            implicant_form = self._pattern_to_form(implicant.pattern, variable_names)
            table_rows.append([implicant_form, *marks])
        return self._format_table(headers, table_rows)

    def karnaugh_text(self, info):
        kmap = info["map"]
        variable_names = info["variable_names"]
        headers = ["implicant", *kmap["cols"]]
        table_rows = []
        for row_name, row in zip(kmap["rows"], kmap["values"]):
            table_rows.append([row_name, *[str(v) for v in row]])
        lines = [self._format_table(headers, table_rows)]
        group_forms = [self._pattern_to_form(item, variable_names) for item in info["groups"]]
        lines.append("Группы: " + ", ".join(group_forms))
        lines.append("Минимизированная ДНФ: " + info["expression"])
        return "\n".join(lines)

    def _patterns(self, implicants, variable_names):
        if not implicants:
            return "[]"
        forms = [self._pattern_to_form(item.pattern, variable_names) for item in implicants]
        return "[" + ", ".join(forms) + "]"

    def _pattern_to_form(self, pattern, variable_names):
        parts = []
        for name, symbol in zip(variable_names, pattern):
            if symbol == "-":
                parts.append("X")
            elif symbol == "1":
                parts.append(name)
            else:
                parts.append(f"!{name}")
        if not parts:
            return "1"
        if len(parts) == 1:
            return parts[0]
        return "(" + " & ".join(parts) + ")"

    def _minterm_form(self, index, variable_names):
        parts = []
        count = len(variable_names)
        for offset, name in enumerate(variable_names):
            bit = (index >> (count - 1 - offset)) & 1
            parts.append(name if bit == 1 else f"!{name}")
        return "(" + " & ".join(parts) + ")"

    def _format_table(self, headers, rows):
        columns = [headers] + rows
        widths = []
        for col_index in range(len(headers)):
            max_width = max(len(str(row[col_index])) for row in columns)
            widths.append(max_width)
        lines = []
        header_cells = [
            str(value).ljust(widths[index]) for index, value in enumerate(headers)
        ]
        lines.append(" | ".join(header_cells))
        separator = ["-" * width for width in widths]
        lines.append("-+-".join(separator))
        for row in rows:
            row_cells = [
                str(value).ljust(widths[index]) for index, value in enumerate(row)
            ]
            lines.append(" | ".join(row_cells))
        return "\n".join(lines)
