class IEEENumber:
    def __init__(self, bits=None):
        if bits is None:
            self.bits = [0] * 32
        else:
            self.bits = bits[:]

    def copy(self):
        return IEEENumber(self.bits[:])

    def get_sign(self):
        return self.bits[0]

    def get_exponent_bits(self):
        return self.bits[1:9]

    def get_mantissa_bits(self):
        return self.bits[9:32]

    def print_in_ieee_format(self):
        print(self.bits[0], end=" ")
        for b in self.bits[1:9]:
            print(b, end="")
        print(" ", end="")
        for b in self.bits[9:32]:
            print(b, end="")
        print()

    def get_bits_str(self):
        return "".join(str(bit) for bit in self.bits)

    def from_bits_to_decimal(self):
        sign = self.bits[0]
        exponent_bits = self.bits[1:9]
        mantissa_bits = self.bits[9:]

        exponent_decimal = 0
        for bit in exponent_bits:
            exponent_decimal = exponent_decimal * 2 + bit

        bias = 127
        if exponent_decimal == 0 and all(b == 0 for b in mantissa_bits):
            return -0.0 if sign == 1 else 0.0
        if exponent_decimal == 255 and all(b == 0 for b in mantissa_bits):
            return float("-inf") if sign == 1 else float("inf")
        if exponent_decimal == 255 and any(b == 1 for b in mantissa_bits):
            return float("nan")

        if exponent_decimal == 0:
            exponent = 1 - bias
            mantissa = 0.0
        else:
            exponent = exponent_decimal - bias
            mantissa = 1.0

        power = 0.5
        for bit in mantissa_bits:
            if bit == 1:
                mantissa += power
            power /= 2

        value = mantissa * (2**exponent)
        if sign == 1:
            value = -value

        return value
