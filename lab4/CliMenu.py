from HashTable import HashTable
from TablePrinter import TablePrinter


class CliMenu:
    def __init__(self) -> None:
        self._table = HashTable()
        self._printer = TablePrinter()

    def run(self) -> None:
        self._maybe_resize()
        while True:
            self._print_menu()
            choice = input("Выберите пункт: ").strip()
            if choice == "1":
                self._insert()
            elif choice == "2":
                self._find()
            elif choice == "3":
                self._update()
            elif choice == "4":
                self._delete()
            elif choice == "5":
                self._printer.print_table(self._table)
            elif choice == "6":
                print(f"Коэффициент заполнения: {self._table.load_factor():.2f}")
            elif choice == "7":
                self._show_v_h()
            elif choice == "0":
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
        raw = input(f"Размер таблицы (по умолчанию {self._table.size}): ").strip()
        if not raw:
            return
        try:
            size = int(raw)
            self._table = HashTable(size=size)
        except ValueError:
            print("Некорректный размер, используется значение по умолчанию.")

    def _insert(self) -> None:
        key = input("Ключ (ID): ").strip()
        value = input("Данные (Pi): ").strip()
        try:
            self._table.insert(key, value)
            print("Запись добавлена.")
        except (KeyError, OverflowError, ValueError, TypeError) as exc:
            print(f"Ошибка: {exc}")

    def _find(self) -> None:
        key = input("Ключ (ID): ").strip()
        try:
            value = self._table.get(key)
            v_value = self._table.calculate_v(key)
            h_value = self._table.calculate_h(key)
            print(f"Найдено: Pi={value}, V(K)={v_value}, h(V)={h_value}")
        except (KeyError, ValueError, TypeError) as exc:
            print(f"Ошибка: {exc}")

    def _update(self) -> None:
        key = input("Ключ (ID): ").strip()
        value = input("Новые данные (Pi): ").strip()
        try:
            self._table.update(key, value)
            print("Запись обновлена.")
        except (KeyError, ValueError, TypeError) as exc:
            print(f"Ошибка: {exc}")

    def _delete(self) -> None:
        key = input("Ключ (ID): ").strip()
        try:
            self._table.delete(key)
            print("Запись удалена.")
        except (KeyError, ValueError, TypeError) as exc:
            print(f"Ошибка: {exc}")

    def _show_v_h(self) -> None:
        key = input("Ключ (ID): ").strip()
        try:
            v_value = self._table.calculate_v(key)
            h_value = self._table.calculate_h(key)
            print(f"V(K)={v_value}, h(V)={h_value}")
        except (ValueError, TypeError) as exc:
            print(f"Ошибка: {exc}")


if __name__ == "__main__":
    CliMenu().run()
