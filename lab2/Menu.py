from services.FunctionAnalyzator import FunctionAnalyzator
from ResultFormatter import ResultFormatter

class Menu:
    def __init__(self):
        self.facade = FunctionAnalyzator()
        self.formatter = ResultFormatter()
        self.actions = self._build_actions()

    def run(self):
        while True:
            self._print_menu()
            option = input("Выберите пункт: ").strip()
            if option == "0":
                print("Завершение работы")
                return
            self._handle(option)

    def _print_menu(self):
        print("\nМеню:")
        print("1. Ввести исходную функцию")
        print("2. Вывести исходную функцию и анализ формы")
        print("3. Построить таблицу истинности")
        print("4. Построить СДНФ/СКНФ, числовую и индексную формы")
        print("5. Определить принадлежность к классам Поста")
        print("6. Построить полином Жегалкина")
        print("7. Найти фиктивные переменные")
        print("8. Булева дифференциация")
        print("9. Минимизация расчетным методом")
        print("10. Минимизация расчетно-табличным методом")
        print("11. Минимизация картой Карно")
        print("12. Выполнить полный анализ")
        print("0. Выход")

    def _handle(self, option):
        try:
            action = self.actions.get(option)
            if action is None:
                print("Неизвестный пункт меню")
                return
            action()
        except ValueError as error:
            print(f"Ошибка: {error}")

    def _build_actions(self):
        return {
            "1": self._input_expression,
            "2": self._show_shape,
            "3": self._show_truth_table,
            "4": self._show_canonical,
            "5": self._show_post,
            "6": self._show_zhegalkin,
            "7": self._show_fictive,
            "8": self._show_derivative,
            "9": self._show_calc_minimization,
            "10": self._show_tabular_minimization,
            "11": self._show_karnaugh,
            "12": self._show_all,
        }

    def _input_expression(self):
        expression = input("Введите логическую функцию (!, &, |, ->, ~): ").strip()
        definition = self.facade.set_expression(expression)
        print("Функция сохранена. Переменные: " + ", ".join(definition.variables))

    def _show_shape(self):
        print(self.formatter.shape_text(self.facade.shape()))

    def _show_truth_table(self):
        definition = self.facade.definition()
        table = self.facade.truth_table()
        print(self.formatter.truth_table_text(table, definition.variables))

    def _show_canonical(self):
        print(self.formatter.canonical_text(self.facade.canonical()))

    def _show_post(self):
        print(self.formatter.post_text(self.facade.post()))

    def _show_zhegalkin(self):
        print("Полином Жегалкина: " + self.facade.zhegalkin())

    def _show_fictive(self):
        fictive = self.facade.fictive()
        if fictive:
            print("Фиктивные переменные: " + ", ".join(fictive))
        else:
            print("Фиктивных переменных нет")

    def _show_derivative(self):
        text = input("Введите переменные для производной через запятую: ").strip()
        variables = tuple(item.strip() for item in text.split(",") if item.strip())
        print(self.formatter.derivative_text(self.facade.derivative(variables)))

    def _show_calc_minimization(self):
        info = self.facade.minimize_calculation()
        print(self.formatter.minimization_text(info))

    def _show_tabular_minimization(self):
        info = self.facade.minimize_tabular()
        print(self.formatter.minimization_text(info))
        print(self.formatter.tabular_chart_text(info))

    def _show_karnaugh(self):
        print(self.formatter.karnaugh_text(self.facade.minimize_karnaugh()))

    def _show_all(self):
        self._show_shape()
        self._show_truth_table()
        self._show_canonical()
        self._show_post()
        self._show_zhegalkin()
        self._show_fictive()
        definition = self.facade.definition()
        default_vars = definition.variables[: min(2, len(definition.variables))]
        print(self.formatter.derivative_text(self.facade.derivative(default_vars)))
        self._show_calc_minimization()
        self._show_tabular_minimization()
        self._show_karnaugh()
