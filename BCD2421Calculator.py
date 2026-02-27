from exceptions import BCD2421Error


class BCD2421Calculator:
    DIGITS_TO_2421 = {
        0: (0, 0, 0, 0),
        1: (0, 0, 0, 1),
        2: (0, 0, 1, 0),
        3: (0, 0, 1, 1),
        4: (0, 1, 0, 0),
        5: (1, 0, 1, 1),
        6: (1, 1, 0, 0),
        7: (1, 1, 0, 1),
        8: (1, 1, 1, 0),
        9: (1, 1, 1, 1),
    }

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
        a_digit = self.bits_to_digits(a_bits)[0]
        b_digit = self.bits_to_digits(b_bits)[0]

        sum = a_digit + b_digit + carry_in
        if sum >= 10:
            sum -= 10
            carry_out = 1
        else:
            carry_out = 0

        return list(self.DIGITS_TO_2421[sum]), carry_out

    def add_numbers(self, a_digits, b_digits):
        max_len = max(len(a_digits), len(b_digits))
        a_digits = [0] * (max_len - len(a_digits)) + a_digits
        b_digits = [0] * (max_len - len(b_digits)) + b_digits

        a_bits = []
        b_bits = []
        for d in a_digits:
            a_bits.extend(self.DIGITS_TO_2421[d])
        for d in b_digits:
            b_bits.extend(self.DIGITS_TO_2421[d])

        result_bits = []
        carry = 0
        for i in range(max_len - 1, -1, -1):
            a_part = a_bits[i*4:(i+1)*4]
            b_part = b_bits[i*4:(i+1)*4]
            sum_part_number, carry = self.add_single_digit(a_part, b_part, carry)
            result_bits = sum_part_number + result_bits

        if carry:
            result_bits = list(self.DIGITS_TO_2421[carry]) + result_bits

        result_digits = self.bits_to_digits(result_bits)
        return result_bits, result_digits
