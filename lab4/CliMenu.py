try:
    from .HashTable import HashTable
    from .TablePrinter import TablePrinter
except ImportError:  # fallback for direct execution
    from HashTable import HashTable
    from TablePrinter import TablePrinter


class CliMenu:
    def __init__(self) -> None:
        self._hash_table = HashTable()
        self._table_printer = TablePrinter()

    def run(self) -> None:
        self._maybe_resize()
        while True:
            self._print_menu()
            menu_choice = input("Выберите пункт: ").strip()
            if menu_choice == "1":
                self._insert()
            elif menu_choice == "2":
                self._find()
            elif menu_choice == "3":
                self._update()
            elif menu_choice == "4":
                self._delete()
            elif menu_choice == "5":
                self._table_printer.print_table(self._hash_table)
            elif menu_choice == "6":
                print(f"Коэффициент заполнения: {self._hash_table.load_factor():.2f}")
            elif menu_choice == "7":
                self._show_v_h()
            elif menu_choice == "0":
                print("Выход.")
                break
            else:
                print("Неверный пункт меню.")

    def _print_menu(self) -> None:
        print("\nМеню:")
        print("1. Добавить запись")
        print("2. Найти запись")
        print("3. Обновить запись")
        print("4. Удалить запись")
        print("5. Показать таблицу")
        print("6. Показать коэффициент заполнения")
        print("7. Показать V(K) и h(V) для ключа")
        print("0. Выход")

    def _maybe_resize(self) -> None:
        raw_value = input(
            f"Размер таблицы (по умолчанию {self._hash_table.size}): "
        ).strip()
        if not raw_value:
            return
        try:
            table_size = int(raw_value)
            self._hash_table = HashTable(size=table_size)
        except ValueError:
            print("Некорректный размер, используется значение по умолчанию.")

    def _insert(self) -> None:
        identifier = input("Ключ (ID): ").strip()
        payload = input("Данные (Pi): ").strip()
        try:
            self._hash_table.insert(identifier, payload)
            print("Запись добавлена.")
        except (KeyError, OverflowError, ValueError, TypeError) as exc:
            print(f"Ошибка: {exc}")

    def _find(self) -> None:
        identifier = input("Ключ (ID): ").strip()
        try:
            payload = self._hash_table.get(identifier)
            numeric_value = self._hash_table.calculate_value(identifier)
            hash_address = self._hash_table.calculate_address(identifier)
            print(f"Найдено: Pi={payload}, V(K)={numeric_value}, h(V)={hash_address}")
        except (KeyError, ValueError, TypeError) as exc:
            print(f"Ошибка: {exc}")

    def _update(self) -> None:
        identifier = input("Ключ (ID): ").strip()
        payload = input("Новые данные (Pi): ").strip()
        try:
            self._hash_table.update(identifier, payload)
            print("Запись обновлена.")
        except (KeyError, ValueError, TypeError) as exc:
            print(f"Ошибка: {exc}")

    def _delete(self) -> None:
        identifier = input("Ключ (ID): ").strip()
        try:
            self._hash_table.delete(identifier)
            print("Запись удалена.")
        except (KeyError, ValueError, TypeError) as exc:
            print(f"Ошибка: {exc}")

    def _show_v_h(self) -> None:
        identifier = input("Ключ (ID): ").strip()
        try:
            numeric_value = self._hash_table.calculate_value(identifier)
            hash_address = self._hash_table.calculate_address(identifier)
            print(f"V(K)={numeric_value}, h(V)={hash_address}")
        except (ValueError, TypeError) as exc:
            print(f"Ошибка: {exc}")


if __name__ == "__main__":
    CliMenu().run()
