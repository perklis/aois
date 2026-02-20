from NumbersConverter import NumbersConverter


class Calculator:

    def __init__(self, x: NumbersConverter, y: NumbersConverter) -> None:
        self.x = x
        self.y = y

    def add(self):
        result_bits, _ = NumbersConverter._add_bits(
            self.x.additional_code,
            self.y.additional_code
        )

        overflow = (
            self.x.additional_code[0] == self.y.additional_code[0]
            and result_bits[0] != self.x.additional_code[0]
        )

        result_int = NumbersConverter.additional_code_to_int(result_bits)
        return NumbersConverter(result_int), overflow

    def subtract(self):
        neg_y = self._negate(self.y.additional_code)

        result_bits, _ = NumbersConverter._add_bits(
            self.x.additional_code,
            neg_y
        )

        overflow = (
            self.x.additional_code[0] != self.y.additional_code[0]
            and result_bits[0] != self.x.additional_code[0]
        )

        result_int = NumbersConverter.additional_code_to_int(result_bits)
        return NumbersConverter(result_int), overflow

    def multiply(self):

        a = self.x.direct_code
        b = self.y.direct_code

        sign = a[0] ^ b[0]

        mag_a = a[1:]
        mag_b = b[1:]

        result = [0] * 31

        for i in range(30, -1, -1):
            if mag_b[i] == 1:

                shifted = mag_a.copy()

                for _ in range(30 - i):
                    shifted = shifted[1:] + [0]

                temp, _ = NumbersConverter._add_bits(
                    [0] + result,
                    [0] + shifted
                )
                result = temp[1:]

        value = 0
        for bit in result:
            value = (value << 1) + bit

        if sign == 1:
            value = -value

        return NumbersConverter(value)

    def divide(self):

        a = self.x.direct_code
        b = self.y.direct_code

        if all(bit == 0 for bit in b[1:]):
            raise ZeroDivisionError("Деление на 0")

        sign = a[0] ^ b[0]

        dividend = a[1:]
        divisor = b[1:]

        quotient = [0] * 31
        remainder = [0] * 31

        for i in range(31):

            remainder = remainder[1:] + [dividend[i]]

            neg_divisor = self._negate([0] + divisor)
            temp, _ = NumbersConverter._add_bits(
                [0] + remainder,
                neg_divisor
            )

            temp = temp[1:]

            if temp[0] == 0:
                remainder = temp
                quotient[i] = 1

        quotient_value = 0
        for bit in quotient:
            quotient_value = (quotient_value << 1) + bit

        if sign == 1:
            quotient_value = -quotient_value

        remainder_value = 0
        for bit in remainder:
            remainder_value = (remainder_value << 1) + bit

        if a[0] == 1:
            remainder_value = -remainder_value

        return NumbersConverter(quotient_value), NumbersConverter(remainder_value)

    @staticmethod
    def _negate(bits: list[int]) -> list[int]:
        inverted = [0 if b == 1 else 1 for b in bits]
        one = [0] * 31 + [1]
        result, _ = NumbersConverter._add_bits(inverted, one)
        return result