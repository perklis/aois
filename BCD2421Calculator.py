from exceptions import BCD2421Error


class BCD2421Calculator:
    DIGITS_TO_2421 = {
        0: (0, 0, 0, 0),
        1: (0, 0, 0, 1),
        2: (0, 0, 1, 0),
        3: (0, 0, 1, 1),
        4: (0, 1, 0, 0),
        5: (1, 0, 0, 0),
        6: (1, 0, 0, 1),
        7: (1, 0, 1, 0),
        8: (1, 0, 1, 1),
        9: (0, 1, 1, 1),
    }

    def __init__(self):
        self.add_table = {}
        self._build_add_table()

    def _build_add_table(self):
        for a_digit in range(10):
            for b_digit in range(10):
                for carry_in in (0, 1):
                    self.add_table[
                        (
                            self.DIGITS_TO_2421[a_digit],
                            self.DIGITS_TO_2421[b_digit],
                            carry_in,
                        )
                    ] = self._compute_sum(a_digit, b_digit, carry_in)

    @staticmethod
    def _compute_sum(a, b, carry_in):
        sum_carrys = a + b + carry_in
        carry_out = 0
        if sum_carrys >= 10:
            sum_carrys -= 10
            carry_out = 1
        return (sum_carrys, carry_out)

    def digits_to_bits(self, digits):
        bits = []
        for d in digits:
            if d not in self.DIGITS_TO_2421:
                raise BCD2421Error(f"{d} невалидна для BCD 2421")
            bits.extend(self.DIGITS_TO_2421[d])
        return bits

    def bits_to_digits(self, bits):
        if len(bits) % 4 != 0:
            raise BCD2421Error("Количество бит не кратно 4")
        inversed_dict = {v: k for k, v in self.DIGITS_TO_2421.items()}
        digits = []
        for i in range(0, len(bits), 4):
            part = tuple(bits[i : i + 4])
            if part not in inversed_dict:
                raise BCD2421Error(f"{bits[i : i + 4]} невалидна для BCD 2421")
            digits.append(inversed_dict[part])
        return digits

    def add_single_digit(self, a_bits, b_bits, carry_in):
        key = (tuple(a_bits), tuple(b_bits), carry_in)
        if key not in self.add_table:
            raise BCD2421Error(f"Ошибка сложения {a_bits}и {b_bits}")
        sum_digit, carry_out = self.add_table[key]
        return self.DIGITS_TO_2421[sum_digit], carry_out

    def add_numbers(self, a_bits, b_bits):
        if len(a_bits) != len(b_bits):
            raise BCD2421Error("Длина битов должна совпадать")

        result = []
        carry = 0
        for i in range(len(a_bits) - 4, -1, -4):
            a_part = a_bits[i : i + 4]
            b_part = b_bits[i : i + 4]
            sum_chunk, carry = self.add_single_digit(a_part, b_part, carry)
            result = list(sum_chunk) + result

        if carry:
            result = [0, 0, 0, 1] + result
        return result
