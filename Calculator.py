from NumbersConverter import NumbersConverter


class Calculator:
    BITS = 32
    ABS_BITS = 31  # для прямого кода: 1 бит знак + 31 бит модуль

    def __init__(self, x: NumbersConverter, y: NumbersConverter) -> None:
        self.x = x
        self.y = y

    @staticmethod
    def _add_bits(a: str, b: str) -> tuple[str, int]:
        if len(a) != 32 or len(b) != 32:
            raise ValueError("Ожидаются строки по 32 бит")

        carry = 0
        out = ["0"] * 32

        for i in range(31, -1, -1):
            a_bit = 1 if a[i] == "1" else 0
            b_bit = 1 if b[i] == "1" else 0

            s = a_bit + b_bit + carry
            out[i] = "1" if (s % 2) == 1 else "0"
            carry = 1 if s >= 2 else 0

        return "".join(out), carry

    # ---------- операции в дополнительном коде ----------

    def add(self) -> tuple[NumbersConverter, bool]:
        """a + b в дополнительном коде."""
        a = self.x.additional_code
        b = self.y.additional_code

        sum_bits, _ = self._add_bits(a, b)

        # переполнение по знакам
        overflow = (a[0] == b[0]) and (sum_bits[0] != a[0])

        result_int = NumbersConverter.additional_code_to_int(sum_bits)
        return NumbersConverter(result_int), overflow

    def subtract(self) -> tuple[NumbersConverter, bool]:
        """a - b = a + (-b) в дополнительном коде."""
        a_bits = self.x.additional_code
        b_bits = self.y.additional_code

        # -b: инверсия + 1
        b_inverted = ""
        for bit in b_bits:
            b_inverted += "0" if bit == "1" else "1"

        minus_b_bits, _ = self._add_bits(b_inverted, "0" * 31 + "1")

        # a + (-b)
        result_bits, _ = self._add_bits(a_bits, minus_b_bits)

        # переполнение по знакам (a и -b)
        overflow = (a_bits[0] == minus_b_bits[0]) and (result_bits[0] != a_bits[0])

        result_int = NumbersConverter.additional_code_to_int(result_bits)
        return NumbersConverter(result_int), overflow

    # ---------- утилиты для прямого кода ----------

    @staticmethod
    def _binary_to_int_unsigned(bits: str) -> int:
        """Строка бит -> неотрицательное int."""
        val = 0
        for ch in bits:
            val = val * 2 + (1 if ch == "1" else 0)
        return val

    @classmethod
    def _direct_code_to_int(cls, direct32: str) -> int:
        """32-битный прямой код (знак-модуль) -> int."""
        if len(direct32) != cls.BITS:
            raise ValueError("Ожидается прямой код на 32 бита")

        sign = -1 if direct32[0] == "1" else 1
        mag = cls._binary_to_int_unsigned(direct32[1:])  # 31 бит
        return sign * mag

    @staticmethod
    def _add_bits_n(a: str, b: str) -> str:
        """Сложение двух строк одинаковой длины N, возвращает сумму N бит (перенос отбрасывается)."""
        if len(a) != len(b):
            raise ValueError("Для _add_bits_n длины должны совпадать")

        carry = 0
        out = ["0"] * len(a)

        for i in range(len(a) - 1, -1, -1):
            a_bit = 1 if a[i] == "1" else 0
            b_bit = 1 if b[i] == "1" else 0

            s = a_bit + b_bit + carry
            out[i] = "1" if (s % 2) == 1 else "0"
            carry = 1 if s >= 2 else 0

        return "".join(out)

    @staticmethod
    def _shift_left_n(bits: str, positions: int) -> str:
        """Логический сдвиг влево в строке длины N (обрезаем слева, дополняем справа нулями)."""
        n = len(bits)
        if positions <= 0:
            return bits
        if positions >= n:
            return "0" * n
        return bits[positions:] + ("0" * positions)

    # ---------- умножение в прямом коде ----------

    def multiply_direct_code(self, a_int: int, b_int: int) -> tuple[NumbersConverter, bool]:
        """
        Умножение в прямом коде (32 бита, знак-модуль).
        Возвращает (NumbersConverter(результат_в_int), overflow_модуля).
        overflow_модуля=True если модуль результата не помещается в 31 бит.
        """
        a_obj = NumbersConverter(a_int)
        b_obj = NumbersConverter(b_int)

        a_direct = a_obj.direct_code  # 32 бита
        b_direct = b_obj.direct_code

        # знак произведения
        sign_result = "1" if a_direct[0] != b_direct[0] else "0"

        # модули (31 бит)
        mag_a = a_direct[1:].zfill(self.ABS_BITS)
        mag_b = b_direct[1:].zfill(self.ABS_BITS)

        # перемножаем модули (shift-add по битам множителя)
        acc = "0" * self.ABS_BITS  # 31 бит суммы частичных произведений
        for i in range(self.ABS_BITS - 1, -1, -1):  # 30..0
            if mag_b[i] == "1":
                shift = (self.ABS_BITS - 1) - i
                shifted = self._shift_left_n(mag_a, shift)
                acc = self._add_bits_n(acc, shifted)

        # overflow модуля: если настоящее произведение не помещается в 31 бит
        # (проверяем через int, это просто контроль; само умножение выше — бинарное)
        true_mag = abs(a_int) * abs(b_int)
        overflow_mag = true_mag >= (1 << self.ABS_BITS)

        result_direct = sign_result + acc  # 1 + 31 = 32
        result_int = self._direct_code_to_int(result_direct)

        return NumbersConverter(result_int), overflow_mag
