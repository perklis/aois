class NumbersConverter:
    BITS = 32
    ABS_BITS = 31 

    def __init__(self, number: int) -> None:
        self.number = number
        self.direct_code = self.get_direct_code()
        self.reversed_code = self.get_reversed_code()
        self.additional_code = self.get_additional_code()

    @staticmethod
    def decimal_to_binary_value(number: int) -> str:
        if number == 0:
            return "0"

        digits = []
        positive_number = abs(number)
        while positive_number > 0:
            digits.append(str(positive_number % 2))
            positive_number //= 2

        return "".join(reversed(digits))

    def get_direct_code(self) -> str:
        n = self.number

        sign_bit = "0" if n >= 0 else "1"
        mag = self.decimal_to_binary_value(n)

        if len(mag) > self.ABS_BITS:
            print(f"Внимание: {n} не помещается в 32-битный прямой код без переполнения")
            mag = mag[-self.ABS_BITS:]
        else:
            mag = mag.zfill(self.ABS_BITS)

        return sign_bit + mag

    def get_reversed_code(self) -> str:
        n = self.number
        direct = self.direct_code

        if n >= 0:
            return direct

        inverted = ""
        for bit in direct:
            inverted += "1" if bit == "0" else "0"
        return inverted

    def get_additional_code(self) -> str:
        n = self.number
    
        # 32-битное представление для +|n|: 0 + 31 бит модуля
        mag = self.decimal_to_binary_value(abs(n))
        if len(mag) > self.ABS_BITS:
            print(f"Внимание: {n} не помещается в 32-битный дополнительный код без переполнения")
            mag = mag[-self.ABS_BITS:]
        else:
            mag = mag.zfill(self.ABS_BITS)
    
        positive_32 = "0" + mag  # это +|n| в 32 битах
    
        if n >= 0:
            return positive_32
    
        # n < 0: инверсия всех 32 бит + 1
        inverted = ""
        for bit in positive_32:
            inverted += "0" if bit == "1" else "1"
    
        plus1, _ = self._add_bits_32(inverted, "0" * 31 + "1")
        return plus1

    
    @staticmethod
    def _add_bits_32(a: str, b: str) -> tuple[str, int]:
        """Нужно только чтобы сделать '+1' при декодировании отрицательного числа."""
        if len(a) != 32 or len(b) != 32:
            raise ValueError("Ожидаются строки ровно по 32 бита")

        carry = 0
        out = ["0"] * 32

        for i in range(31, -1, -1):
            a_bit = 1 if a[i] == "1" else 0
            b_bit = 1 if b[i] == "1" else 0
            s = a_bit + b_bit + carry
            out[i] = "1" if (s % 2) == 1 else "0"
            carry = 1 if s >= 2 else 0

        return "".join(out), carry

    @staticmethod
    def _binary_str_to_int_unsigned(bits: str) -> int:
        value = 0
        for ch in bits:
            value = value * 2 + (1 if ch == "1" else 0)
        return value

    @staticmethod
    def _add_bits(a: str, b: str) -> tuple[str, int]:
        """Нужно только чтобы сделать '+1' при декодировании отрицательного числа."""
        if len(a) != 32 or len(b) != 32:
            raise ValueError("Ожидаются строки ровно по 32 бита")

        carry = 0
        out = ["0"] * 32

        for i in range(31, -1, -1):
            a_bit = 1 if a[i] == "1" else 0
            b_bit = 1 if b[i] == "1" else 0
            s = a_bit + b_bit + carry
            out[i] = "1" if (s % 2) == 1 else "0"
            carry = 1 if s >= 2 else 0

        return "".join(out), carry

    @staticmethod
    def _binary_str_to_int(bits: str) -> int:
        value = 0
        for ch in bits:
            value = value * 2 + (1 if ch == "1" else 0)
        return value
    
    @classmethod
    def additional_code_to_int(cls, code32: str) -> int:
        """Перевод 32-битной строки дополнительного кода в int."""
        if len(code32) != cls.BITS:
            raise ValueError("Ожидается строка на 32 бита")
        for ch in code32:
            if ch not in "01":
                raise ValueError("Строка должна состоять только из '0' и '1'")

        if code32[0] == "0":
            return cls._binary_str_to_int_unsigned(code32)

        inverted = ""
        for ch in code32:
            inverted += "0" if ch == "1" else "1"

        plus1, _ = cls._add_bits_32(inverted, "0" * 31 + "1")
        magnitude = cls._binary_str_to_int_unsigned(plus1)
        return -magnitude

    def __str__(self) -> str:
        return (
            f"Число {self.number}\n"
            f"-Прямой:     {self.direct_code}\n"
            f"-Обратный:   {self.reversed_code}\n"
            f"-Дополнительный: {self.additional_code}"
        )


