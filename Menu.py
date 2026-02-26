from NumbersConverter import NumbersConverter
from Calculator import Calculator
from IEEECalculator import IEEECalculator
from BCD2421Calculator import BCD2421Calculator
from exceptions import BCD2421Error, DivisionByZeroError


class Menu:
    def __init__(self):
        self.running = True
        self.calc_type = None
        self.a = None
        self.b = None
        self.calc = None
        self.ieee_calc = None

    def run(self):
        self.select_calculator()
        self.input_numbers()

        while self.running:
            try:
                self.print_menu()
                choice = input("Выберите пункт: ").strip()
                self.handle_choice(choice)
            except ValueError:
                print("Ошибка ввода")
            except DivisionByZeroError:
                print("Ошибка: деление на 0")
            except KeyboardInterrupt:
                print("\nВыход")
                self.running = False

    def select_calculator(self):
        while True:
            print("Выберите калькулятор:")
            print("1 - Обычный")
            print("2 - По стандарту IEEE-754-2008")
            print("3 - b)2421 BCD")

            choice = input("Ваш выбор: ").strip()

            if choice == "1":
                self.calc_type = "normal"
                self.calc = Calculator()
                break
            if choice == "2":
                self.calc_type = "ieee"
                self.ieee_calc = IEEECalculator()
                break
            if choice == "3":
                self.calc_type = "bcd"
                self.bcd_calc = BCD2421Calculator()
                break
            print("Неверный выбор, попробуйте снова")

    def input_numbers(self):
        while True:
            try:
                a_input = input("Введите первое число: ").strip().replace(" ", "")
                b_input = input("Введите второе число: ").strip().replace(" ", "")

                if self.calc_type == "normal":
                    self.a = NumbersConverter.from_decimal_to_direct_code(int(a_input))
                    self.b = NumbersConverter.from_decimal_to_direct_code(int(b_input))
                    return

                if self.calc_type == "ieee":
                    self.a = self.ieee_calc.decimal_to_ieee(a_input)
                    self.b = self.ieee_calc.decimal_to_ieee(b_input)
                    return

                if self.calc_type == "bcd":
                    self.a = [int(d) for d in a_input]
                    self.b = [int(d) for d in b_input]
                    return

            except ValueError:
                print("Введите корректные числа")

    def print_menu(self):
        print("\nТекущие числа:")

        if self.calc_type == "normal":
            print("A =", self.a.from_direct_code_to_decimal())
            print("B =", self.b.from_direct_code_to_decimal())

        if self.calc_type == "ieee":
            print("A:", self.a.get_bits_str())
            print("A:", self.a.from_bits_to_decimal())

            print("B:", self.b.get_bits_str())
            print("B:", self.b.from_bits_to_decimal())

        if self.calc_type == "bcd":
            print("A:", self.a)
            print("A:", self.bcd_calc.digits_to_bits(self.a))
            print("B:", self.b)
            print("B:", self.bcd_calc.digits_to_bits(self.b))

        print("\nВыберите операцию:")

        if self.calc_type == "normal":
            print("1. Показать прямой, обратный, дополнительный код")
            print("2. Сложение")
            print("3. Вычитание")
            print("4. Умножение")
            print("5. Деление")

        if self.calc_type == "ieee":
            print("1. Сложение")
            print("2. Вычитание")
            print("3. Умножение")
            print("4. Деление")

        if self.calc_type == "bcd":
            print("1. Сложение BCD 2421")

        print("6. Ввести числа заново")
        print("0. Выход")

    def handle_choice(self, choice):

        if self.calc_type == "normal":
            self._handle_normal(choice)

        elif self.calc_type == "ieee":
            self._handle_ieee(choice)

        elif self.calc_type == "bcd":
            self._handle_bcd(choice)

    def _handle_normal(self, choice):

        if choice == "1":
            print("\nЧИСЛО A")
            print(self.a)
            print("\nЧИСЛО B")
            print(self.b)
            return

        if choice == "2":
            print("\nСЛОЖЕНИЕ")
            print(self.calc.add(self.a, self.b))
            return

        if choice == "3":
            print("\nВЫЧИТАНИЕ")
            print(self.calc.subtract(self.a, self.b))
            return

        if choice == "4":
            print("\nУМНОЖЕНИЕ")
            print(self.calc.multiply(self.a, self.b))
            return

        if choice == "5":
            result = self.calc.divide(self.a, self.b)
            print("\nДЕЛЕНИЕ")
            print("Десятичное:", result.to_decimal_division())
            print("Прямой:       ", result.get_direct_code())
            print("Обратный:     ", result.get_ones_complement())
            print("Дополнительный:", result.get_twos_complement())
            return

        if choice == "6":
            self.input_numbers()
            return

        if choice == "0":
            self.running = False
            return

        print("Попробуй снова")

    def _handle_ieee(self, choice):

        if choice == "1":
            result = self.ieee_calc.add(self.a, self.b)
            operation_name = "СЛОЖЕНИЕ"

        elif choice == "2":
            result = self.ieee_calc.subtract(self.a, self.b)
            operation_name = "ВЫЧИТАНИЕ"

        elif choice == "3":
            result = self.ieee_calc.multiply(self.a, self.b)
            operation_name = "УМНОЖЕНИЕ"

        elif choice == "4":
            result = self.ieee_calc.divide(self.a, self.b)
            operation_name = "ДЕЛЕНИЕ"

        elif choice == "6":
            self.input_numbers()
            return

        elif choice == "0":
            self.running = False
            print("Выход")
            return

        else:
            print("Неверный пункт меню")
            return

        print(f"\n{operation_name}")

        print("\nA:")
        print("  Двоичный:", self.a.get_bits_str())
        print("  Десятичный:", self.a.from_bits_to_decimal())

        print("\nB:")
        print("  Двоичный:", self.b.get_bits_str())
        print("  Десятичный:", self.b.from_bits_to_decimal())

        print("\nОтвет:")
        print("  Двоичный:", result.get_bits_str())
        print("  Десятичный:", result.from_bits_to_decimal())

    def _handle_bcd(self, choice):
        if choice == "1":
            try:
                max_len = max(len(self.a), len(self.b))
                a_digits = [0] * (max_len - len(self.a)) + self.a
                b_digits = [0] * (max_len - len(self.b)) + self.b

                a_bits = self.bcd_calc.digits_to_bits(a_digits)
                b_bits = self.bcd_calc.digits_to_bits(b_digits)

                result_bits = self.bcd_calc.add_numbers(a_bits, b_bits)
                result_digits = self.bcd_calc.bits_to_digits(result_bits)

                print("\nСЛОЖЕНИЕ BCD 2421")
                print("A:", a_digits)
                print("A в битах:", a_bits)
                print("B:", b_digits)
                print("B в битах:", b_bits)
                print("Результат:", result_digits)
                print("Результат в битах:", result_bits)

            except BCD2421Error as e:
                print("Ошибка ввода:", e)
        elif choice == "6":
            self.input_numbers()
            return
        elif choice == "0":
            self.running = False
            print("Выход")
            return
        else:
            print("Неверный пункт меню")
