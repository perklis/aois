class ResultFormatter:
    def shape_text(self, shape):
        lines = ["Анализ исходной функции:"]
        lines.append(f"- Выражение: {shape['source']}")
        lines.append(f"- Переменные: {', '.join(shape['variables'])}")
        lines.append(f"- Количество переменных: {shape['count']}")
        lines.append(f"- Одиночное отрицание: {shape['has_single_negation']}")
        lines.append(f"- Групповое отрицание: {shape['has_group_negation']}")
        return "\n".join(lines)

    def truth_table_text(self, rows, variable_names):
        head = " | ".join(["idx", *variable_names, "f"])
        lines = [head, "-" * len(head)]
        for row in rows:
            values = [str(row.index)]
            values.extend(str(row.assignment[name]) for name in variable_names)
            values.append(str(row.value))
            lines.append(" | ".join(values))
        return "\n".join(lines)

    def canonical_text(self, info):
        lines = ["Канонические формы:"]
        lines.append(f"- СДНФ: {info['sdnf']}")
        lines.append(f"- СКНФ: {info['sknf']}")
        lines.append(f"- Числовая форма СДНФ: {info['numeric_sdnf']}")
        lines.append(f"- Числовая форма СКНФ: {info['numeric_sknf']}")
        lines.append(f"- Индексная форма (вектор): {info['index_binary']}")
        lines.append(f"- Индексная форма (число): {info['index_decimal']}")
        lines.append(f"- Проверка конституент СДНФ: {info['sdnf_constituents_ok']}")
        lines.append(f"- Проверка конституент СКНФ: {info['sknf_constituents_ok']}")
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
            f"Производная по [{variables}]",
            f"  Вектор: {vec}",
            f"  СДНФ: {info['sdnf']}",
            f"  Упрощенная формула: {info['simplified_sdnf']}",
        ])

    def minimization_text(self, info):
        lines = ["Этапы склеивания:"]
        for index, stage in enumerate(info["stages"], start=1):
            text = ", ".join(f"{item.pattern}:{item.minterms}" for item in stage)
            lines.append(f"- Этап {index}: [{text}]")
        lines.append("Простые импликанты: " + self._implicants(info["prime"]))
        lines.append("Выбранные импликанты: " + self._implicants(info["selected"]))
        lines.append("Минимизированная ДНФ: " + info["expression"])
        return "\n".join(lines)

    def tabular_chart_text(self, info):
        chart = info["chart"]
        if not chart["minterms"]:
            return "Таблица покрытия: нет минтермов"
        head = "implicant | " + " | ".join(str(v) for v in chart["minterms"])
        lines = [head, "-" * len(head)]
        for implicant, row in zip(chart["implicants"], chart["matrix"]):
            marks = ["X" if value == 1 else "." for value in row]
            lines.append(implicant.pattern + " | " + " | ".join(marks))
        return "\n".join(lines)

    def karnaugh_text(self, info):
        kmap = info["map"]
        head = "row/col | " + " | ".join(kmap["cols"])
        lines = [head, "-" * len(head)]
        for row_name, row in zip(kmap["rows"], kmap["values"]):
            lines.append(row_name + " | " + " | ".join(str(v) for v in row))
        lines.append("Группы (по выбранным импликантам): " + ", ".join(info["groups"]))
        lines.append("Минимизированная ДНФ: " + info["expression"])
        return "\n".join(lines)

    def _implicants(self, implicants):
        if not implicants:
            return "[]"
        return "[" + ", ".join(f"{i.pattern}:{i.minterms}" for i in implicants) + "]"
