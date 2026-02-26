from NumbersConverter import NumbersConverter, SCALE, FRAC_BITS
from BitOperations import BitOperations

class Calculator:

    def __init__(self):
        self.bits=BitOperations()

    def add(self, a: NumbersConverter, b: NumbersConverter):
        list_twos1 = a.get_twos_complement()
        list_twos2 = b.get_twos_complement()
        result = [0] * 32
        result, _ = self.bits.add_bits(list_twos1, list_twos2)
            
        return NumbersConverter.from_twos_to_direct(result)

    def subtract(self, a, b):
        return self.add(a, self.negate(b))

    def negate(self, number: NumbersConverter):
        twos_complement_number = number.get_twos_complement()
        inverted = [1 - b for b in twos_complement_number]
        carry = 1
        for i in reversed(range(32)):
            sum = inverted[i] + carry
            inverted[i] = sum % 2
            carry = sum // 2
        return NumbersConverter.from_twos_to_direct(inverted)

    def multiply(self, a: NumbersConverter, b: NumbersConverter):
        sign = 0
        if a.bits[0] != b.bits[0]:
            sign = 1
        result = [0] * 32
        for i in reversed(range(1, 32)):
            if a.bits[i] == 1:
                b_bits_copy = b.bits[:]
                shift = 31 - i
                for _ in range(shift):
                    self.bits.move_left(b_bits_copy)
                result = self.add_direct(result, b_bits_copy)
        result[0] = sign
        return NumbersConverter(result)

    def divide(self, dividend: NumbersConverter, divisor: NumbersConverter):
        if self.is_zero(divisor.bits):
            raise ZeroDivisionError("Деление на 0")

        sign = dividend.bits[0] ^ divisor.bits[0]

        dividend_mag = dividend.bits[1:]
        divisor_mag = divisor.bits[1:]
        remainder = [0] * 31
        quotient_full = []

        total_steps = 31 + FRAC_BITS
        for i in range(total_steps):
            if i < 31:
                next_bit = dividend_mag[i]
            else:
                next_bit = 0
            remainder = remainder[1:] + [next_bit]

            if self.bits.compare_register(remainder, divisor_mag) >= 0:
                remainder = self.bits.sub_register(remainder, divisor_mag)
                quotient_full.append(1)
            else:
                quotient_full.append(0)

        scaled_result = quotient_full[FRAC_BITS:FRAC_BITS + 31]

        result_bits = [0] * 32
        result_bits[0] = sign
        result_bits[1:] = scaled_result

        return NumbersConverter(result_bits)

    def add_direct(self, a, b):
        result = a[:]
        carry = 0
        for i in reversed(range(32)):
            s = result[i] + b[i] + carry
            result[i] = s % 2
            carry = s // 2
        return result

    def is_zero(self, bits):
        return all(b == 0 for b in bits[1:])
