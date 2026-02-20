class NumbersConverter:
    BITS = 32
    ABS_BITS = 31

    def __init__(self, number: int) -> None:
        self.number = number
        self.direct_code = self._get_direct_code()
        self.reversed_code = self._get_reversed_code()
        self.additional_code = self._get_additional_code()

    @staticmethod
    def _decimal_to_binary_abs(n: int) -> list[int]:
        if n == 0:
            return [0]

        bits = []
        n = abs(n)

        while n > 0:
            remainder = n - (n >> 1 << 1) 
            bits.append(remainder)
            n = n >> 1                   

        bits.reverse()
        return bits

    def _get_direct_code(self) -> list[int]:
        sign = 0 if self.number >= 0 else 1
        mag = self._decimal_to_binary_abs(self.number)

        if len(mag) > self.ABS_BITS:
            mag = mag[-self.ABS_BITS:]
        else:
            mag = [0] * (self.ABS_BITS - len(mag)) + mag

        return [sign] + mag

    def _get_reversed_code(self) -> list[int]:
        if self.number >= 0:
            return self.direct_code.copy()

        inverted = [self.direct_code[0]]
        for bit in self.direct_code[1:]:
            inverted.append(0 if bit == 1 else 1)

        return inverted

    def _get_additional_code(self) -> list[int]:
        if self.number >= 0:
            return self.direct_code.copy()

        inverted = [1] 

        for bit in self.direct_code[1:]:
            inverted.append(0 if bit == 1 else 1)

        one = [0] * 31 + [1]
        result, _ = self._add_bits(inverted, one)
        return result

    @staticmethod
    def _add_bits(a: list[int], b: list[int]) -> tuple[list[int], int]:
        carry = 0
        result = [0] * 32

        for i in range(31, -1, -1):
            s = a[i] + b[i] + carry
            result[i] = s & 1
            carry = 1 if s > 1 else 0

        return result, carry

    @classmethod
    def additional_code_to_int(cls, code: list[int]) -> int:

        if code[0] == 0:
            value = 0
            for bit in code:
                value = (value << 1) + bit
            return value

        inverted = [0 if b == 1 else 1 for b in code]

        one = [0] * 31 + [1]
        plus1, _ = cls._add_bits(inverted, one)

        value = 0
        for bit in plus1:
            value = (value << 1) + bit

        return -value

    @staticmethod
    def _binary_to_int_unsigned(bits: list[int]) -> int:
        value = 0
        for bit in bits:
            value = (value << 1) + bit
        return value

    def __str__(self) -> str:
        return (
            f"\nЧисло: {self.number}\n"
            f"Прямой код:        {self.direct_code}\n"
            f"Обратный код:      {self.reversed_code}\n"
            f"Дополнительный код:{self.additional_code}\n"
        )