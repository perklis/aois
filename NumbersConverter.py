from exceptions import InvalidDecimalInputError

FRAC_BITS = 5
SCALE = 10**FRAC_BITS


class NumbersConverter:
    def __init__(self, bits):
        self.bits = bits[:]

    @staticmethod
    def from_decimal_to_direct_code(value):
        if not isinstance(value, int):
            raise InvalidDecimalInputError("Только целые (int) числа разрешены")

        bits = [0] * 32
        if value < 0:
            bits[0] = 1
            value = -value

        i = 31
        while i >= 1:
            bits[i] = value % 2
            value = value // 2
            i -= 1

        return NumbersConverter(bits)

    def from_direct_code_to_decimal(self):
        abs_value = 0
        for i in range(1, 32):
            abs_value = abs_value * 2 + self.bits[i]
        if self.bits[0] == 1:
            abs_value = -abs_value

        return abs_value

    def get_direct_code(self):
        return self.bits[:]

    def get_ones_complement(self):
        result = self.bits[:]
        if result[0] == 1:
            for i in range(1, 32):
                result[i] = 1 - result[i]
        return result

    def get_twos_complement(self):
        result = self.get_ones_complement()
        if result[0] == 0:
            return result
        carry_bit = 1
        for i in reversed(range(32)):
            bit_sum = result[i] + carry_bit
            result[i] = bit_sum % 2
            carry_bit = bit_sum // 2
        return result

    @staticmethod
    def from_twos_to_direct(bits):
        sign = bits[0]
        if sign == 0:
            return NumbersConverter(bits[:])
        inverted_bits = [1 - b for b in bits]
        carry = 1
        for i in reversed(range(32)):
            bit_sum = inverted_bits[i] + carry
            inverted_bits[i] = bit_sum % 2
            carry = bit_sum // 2
        inverted_bits[0] = 1
        return NumbersConverter(inverted_bits)

    def to_decimal_scaled(self, scale=SCALE):
        return self.from_direct_code_to_decimal() / scale

    def __str__(self):
        return (
            "\nДесятичное: "
            + str(self.from_direct_code_to_decimal())
            + "\nПрямой код:        "
            + str(self.get_direct_code())
            + "\nОбратный код:      "
            + str(self.get_ones_complement())
            + "\nДополнительный код:"
            + str(self.get_twos_complement())
            + "\n"
        )
    
    def to_decimal_division(self):
        value = self.from_direct_code_to_decimal()
        return value / (2 ** FRAC_BITS)
