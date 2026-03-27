from typing import Optional

from HashTable import HashTable
from TableEntry import TableEntry


class TablePrinter:
    def print_table(self, table: HashTable) -> None:
        headers = ["Idx", "ID", "V", "h", "C", "U", "D", "Pi"]
        widths = [4, 12, 6, 6, 3, 3, 3, 3, 3, 6, 12]

        line = self._format_row(headers, widths)
        print(line)
        print("-" * len(line))

        for idx, entry in table.rows():
            row = self._row_from_entry(table, idx, entry)
            print(self._format_row(row, widths))

        print("-" * len(line))
        print(f"Load factor: {table.load_factor():.2f}")

    def _row_from_entry(
        self, table: HashTable, idx: int, entry: Optional[TableEntry]
    ) -> list[str]:
        if entry is None:
            return [str(idx), "", "", "", "0", "0", "0", ""]
    
        v_value = table.calculate_v(entry.key)
        h_value = table.calculate_h(entry.key)
    
        return [
            str(idx),
            entry.key,
            str(v_value),
            str(h_value),
            str(entry.collision_flag),
            str(entry.occupied_flag),
            str(entry.deleted_flag),
            str(entry.value),
        ]

    def _format_row(self, columns: list[str], widths: list[int]) -> str:
        padded = [col.ljust(widths[i]) for i, col in enumerate(columns)]
        return " | ".join(padded)
