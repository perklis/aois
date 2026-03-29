from typing import Optional

try:
    from .HashTable import HashTable
    from .TableEntry import TableEntry
except ImportError:  # fallback for direct execution
    from HashTable import HashTable
    from TableEntry import TableEntry


class TablePrinter:
    def print_table(self, hash_table: HashTable) -> None:
        column_headers = ["Idx", "ID", "V", "h", "C", "U", "D", "Pi"]
        column_widths = [4, 12, 6, 6, 3, 3, 3, 3, 3, 6, 12]

        header_line = self._format_row(column_headers, column_widths)
        print(header_line)
        print("-" * len(header_line))

        for row_index, entry in hash_table.rows():
            row_values = self._row_from_entry(hash_table, row_index, entry)
            print(self._format_row(row_values, column_widths))

        print("-" * len(header_line))
        print(f"Load factor: {hash_table.load_factor():.2f}")

    def _row_from_entry(
        self, hash_table: HashTable, row_index: int, entry: Optional[TableEntry]
    ) -> list[str]:
        if entry is None:
            return [str(row_index), "", "", "", "0", "0", "0", ""]

        numeric_value = hash_table.calculate_value(entry.identifier)
        hash_address = hash_table.calculate_address(entry.identifier)

        return [
            str(row_index),
            entry.identifier,
            str(numeric_value),
            str(hash_address),
            str(entry.has_collision),
            str(entry.is_occupied),
            str(entry.is_deleted),
            str(entry.payload),
        ]

    def _format_row(self, columns: list[str], widths: list[int]) -> str:
        padded = [col.ljust(widths[i]) for i, col in enumerate(columns)]
        return " | ".join(padded)
