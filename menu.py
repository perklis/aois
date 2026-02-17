from NumbersConverter import NumbersConverter 
from Calculator import Calculator

class Menu:
    def __init__(self) -> None:
        self._running = True
        self.a: int | None = None
        self.b: int | None = None

    def run(self) -> None:
        self.input_two_numbers()

        while self._running:
            try:
                self.print_menu()
                choice = input("Выберите пункт: ").strip()
                self.handle_choice(choice)
            except ValueError as e:
                print("ValueError:", e)

            except KeyboardInterrupt:
                print("\nВыход.")
                self._running = False

    def input_two_numbers(self) -> None:
        while True:
            try:
                self.a = int(input("Введите первое целое число a: ").strip())
                self.b = int(input("Введите второе целое число b: ").strip())
                return
            except ValueError:
                print("Ошибка: введите два целых числа.")

    def ensure_numbers(self) -> None:
        if self.a is None or self.b is None:
            self.input_two_numbers()

    def print_menu(self) -> None:
        print("\nВыберите:")
        print(f"Текущие числа: a={self.a}, b={self.b}")
        print("1. Перевод в двоичную систему")
        print("2. Сложение a + b")
        print("3. Вычитание a - b")
        print("4. Умножение a * b")
        print("5. Ввести числа заново")
        print("0. Выход")

    def handle_choice(self, choice: str) -> None:
        if choice == "1":
            self.action_convert_both()
        elif choice == "2":
            self.action_add()
        elif choice == "3":
            self.action_sub()
        elif choice == "4":
            self.action_mul_direct()
        elif choice == "5":
            self.input_two_numbers()
        elif choice == "0":
            self.action_exit()
        else:
            print("Попробуйте снова.")

    def action_convert_both(self) -> None:
        self.ensure_numbers()
        assert self.a is not None and self.b is not None

        print("\na:")
        print(NumbersConverter(self.a))

        print("\nb:")
        print(NumbersConverter(self.b))

    def action_add(self) -> None:
        self.ensure_numbers()
        assert self.a is not None and self.b is not None
        num_a = NumbersConverter(self.a)
        num_b = NumbersConverter(self.b)

        calc = Calculator(num_a, num_b)
        result, overflow = calc.add()

        print("\nСложение в дополнительном коде:")
        print(f"{self.a} + {self.b} = {result.number}")
        print(result)
        if overflow:
            print("Переполнение. Результат неверный в 32 битах")


    def action_sub(self) -> None:
        """Вычитание a - b через отрицание и сложение."""
        self.ensure_numbers()
        assert self.a is not None and self.b is not None

        num_a = NumbersConverter(self.a)
        num_b = NumbersConverter(self.b)

        calc = Calculator(num_a, num_b)
        result, overflow = calc.subtract()

        print("\nВычитание в дополнительном коде:")
        print(f"{self.a} - {self.b} = {result.number}")
        print(result)
        if overflow:
            print("Переполнение. Результат неверный в 32 битах")


    def action_mul_direct(self) -> None:
        self.ensure_numbers()
        assert self.a is not None and self.b is not None

        # Для умножения в прямом коде в моём Calculator метод принимает int'ы
        calc = Calculator(NumbersConverter(self.a), NumbersConverter(self.b))
        result, overflow_mag = calc.multiply_direct_code(self.a, self.b)

        print("\nУмножение в прямом коде:")
        print(f"{self.a} * {self.b} = {result.number}")
        print(result)
        if overflow_mag:
            print("Переполнение модуля: результат не помещается в 31 бит прямого кода.")


    def action_exit(self) -> None:
        print("Выход.")
        self._running = False
