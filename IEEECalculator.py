from IEEENumbers import IEEENumber
from BitOperations import BitOperations
from config import MANTISSA_LENGTH, BITS_32, EXP_BITS,EXP_MAX,BIAS 

class IEEECalculator:

    def __init__(self):
        self.bits = BitOperations()

    def _extract_sign(self, number_str):
        sign = 0
        if number_str.startswith("-"):
            sign = 1
            number_str = number_str[1:]
        return sign, number_str

    def _split_parts(self, number_str):
        if "." in number_str:
            return number_str.split(".")
        return number_str, "0"

    def _is_zero(self, int_part_str, frac_part_str):
        return int_part_str.strip("0") == "" and frac_part_str.strip("0") == ""

    def _from_int_part_to_bits(self, int_part_str):
        int_value = 0
        for symb in int_part_str:
            int_value = int_value * 10 + int(symb)
        if int_value == 0:
            return [0]
        bits = []
        while int_value > 0:
            bits.insert(0, int_value % 2)
            int_value //= 2
        return bits

    def _fraction_part_to_bits(self, frac_part_str):
        frac_value = 0
        power = 1
        for c in frac_part_str:
            frac_value = frac_value * 10 + int(c)
            power *= 10
        bits = []
        for _ in range(50):
            frac_value *= 2
            if frac_value >= power:
                bits.append(1)
                frac_value -= power
            else:
                bits.append(0)
        return bits

    def _build_normalized_parts(self, int_bits, frac_bits):
        if int_bits != [0]:
            exponent = len(int_bits) - 1
            mantissa_bits = int_bits[1:] + frac_bits
        else:
            shift = 0
            while shift < len(frac_bits) and frac_bits[shift] == 0:
                shift += 1

            exponent = -(shift + 1)
            mantissa_bits = frac_bits[shift + 1 :]

        exponent += BIAS
        mantissa_bits = mantissa_bits[:MANTISSA_LENGTH]
        while len(mantissa_bits) < MANTISSA_LENGTH:
            mantissa_bits.append(0)

        return exponent, mantissa_bits

    def _build_ieee_number(self, sign, exponent, mantissa_bits):
        exponent_bits = self.bits.int_to_bits(exponent, EXP_BITS)
        return IEEENumber([sign] + exponent_bits + mantissa_bits)

    def decimal_to_ieee(self, number_str: str):
        number_str = number_str.strip().lower()

        if number_str in ("inf", "+inf", "INF", "+INF"):
            return IEEENumber([0] + [1] * EXP_BITS + [0] * MANTISSA_LENGTH)
        if number_str in ("-inf", "-INF"):
            return IEEENumber([1] + [1] * EXP_BITS+ [0] * MANTISSA_LENGTH)
        if number_str in ("nan", "NaN", "NAN"):
            return IEEENumber([0] + [1] * EXP_BITS + [1] + [0] * (MANTISSA_LENGTH - 1))

        sign, number_str = self._extract_sign(number_str)
        int_part_str, frac_part_str = self._split_parts(number_str)

        if self._is_zero(int_part_str, frac_part_str):
            return IEEENumber([sign] + [0] * (BITS_32-1))

        int_bits = self._from_int_part_to_bits(int_part_str)
        frac_bits = self._fraction_part_to_bits(frac_part_str)
        exponent, mantissa_bits = self._build_normalized_parts(int_bits, frac_bits)

        return self._build_ieee_number(sign, exponent, mantissa_bits)

    def _prepare_addition(self, A: IEEENumber, B: IEEENumber):
        sign_a = A.get_sign()
        sign_b = B.get_sign()

        exp_a = self.bits.bits_to_int(A.get_exponent_bits())
        exp_b = self.bits.bits_to_int(B.get_exponent_bits())

        mant_a = self.get_mantissa_with_hidden(A)
        mant_b = self.get_mantissa_with_hidden(B)

        while len(mant_a) < MANTISSA_LENGTH +1:
            mant_a.append(0)
        while len(mant_b) < MANTISSA_LENGTH +1:
            mant_b.append(0)

        return sign_a, sign_b, exp_a, exp_b, mant_a, mant_b

    def _shift_mantisas(self, mant_a, mant_b, exp_a, exp_b):
        if exp_a > exp_b:
            self.bits.move_right(mant_b, exp_a - exp_b)
            return mant_a, mant_b, exp_a
        elif exp_b > exp_a:
            self.bits.move_right(mant_a, exp_b - exp_a)
            return mant_a, mant_b, exp_b
        else:
            return mant_a, mant_b, exp_a

    def _add_or_sub_mantissas(self, mant_a, mant_b, sign_a, sign_b):
        if sign_a == sign_b:
            mant_res, carry = self.bits.add_bits(mant_a, mant_b)
            sign_res = sign_a

            if carry:
                self.bits.move_right(mant_res, 1)
                return mant_res, sign_res, 1
            return mant_res, sign_res, 0
        else:
            if self.bits.compare_register(mant_a, mant_b) == 0:
                return None, 0, 0
            if self.bits.compare_register(mant_a, mant_b) > 0:
                return self.bits.subtract_bits(mant_a, mant_b), sign_a, 0
            else:
                return self.bits.subtract_bits(mant_b, mant_a), sign_b, 0

    def _normalize_after_overflow(self, mant_res, exponent):
        if mant_res[EXP_BITS-1] == 1:
            self.bits.move_right(mant_res, 1)
            exponent += 1

        while mant_res[EXP_BITS] == 0 and exponent > 0:
            self.bits.move_left(mant_res, 1)
            exponent -= 1

        return mant_res, exponent

    def _build_add_result(self, sign_res, exponent, mant_res):
        if exponent >= EXP_MAX:
            return IEEENumber([sign_res] + [1] * EXP_BITS + [0] * MANTISSA_LENGTH)
        if exponent <= 0:
            return IEEENumber([0] * MANTISSA_LENGTH)

        mantissa_bits = mant_res[(EXP_BITS+1):MANTISSA_LENGTH]
        exponent_bits = self.bits.int_to_bits(exponent, EXP_BITS)
        return IEEENumber([sign_res] + exponent_bits + mantissa_bits)

    def is_nan(self, num: IEEENumber):
        exp = self.bits.bits_to_int(num.get_exponent_bits())
        mant = num.get_mantissa_bits()
        return exp == EXP_MAX and any(b == 1 for b in mant)

    def is_infinity(self, num: IEEENumber):
        exp = self.bits.bits_to_int(num.get_exponent_bits())
        mant = num.get_mantissa_bits()
        return exp == EXP_MAX and all(b == 0 for b in mant)

    def add(self, A: IEEENumber, B: IEEENumber):
        if self.is_nan(A) or self.is_nan(B):
            return IEEENumber([0] + [1] * EXP_BITS + [1] + [0] * (MANTISSA_LENGTH-1))

        if self.is_infinity(A):
            if self.is_infinity(B) and A.get_sign() != B.get_sign():
                return IEEENumber([0] + [1] * EXP_BITS + [1] + [0] * (MANTISSA_LENGTH-1))
            return A.copy()
        if self.is_infinity(B):
            return B.copy()
        if self.is_zero(A):
            return B.copy()
        if self.is_zero(B):
            return A.copy()

        sign_a, sign_b, exp_a, exp_b, mant_a, mant_b = self._prepare_addition(A, B)
        mant_a, mant_b, exponent = self._shift_mantisas(mant_a, mant_b, exp_a, exp_b)

        mant_res, sign_res, carry_shift = self._add_or_sub_mantissas(
            mant_a, mant_b, sign_a, sign_b
        )

        if mant_res is None:
            return IEEENumber([0] * BITS_32)

        exponent += carry_shift
        mant_res, exponent = self._normalize_after_overflow(mant_res, exponent)

        return self._build_add_result(sign_res, exponent, mant_res)

    def subtract(self, A: IEEENumber, B: IEEENumber):
        neg_B_bits = B.bits[:]
        neg_B_bits[0] ^= 1
        neg_B = IEEENumber(neg_B_bits)
        return self.add(A, neg_B)

    def is_zero(self, num: IEEENumber) -> bool:
        return all(b == 0 for b in num.get_exponent_bits()) and all(
            b == 0 for b in num.get_mantissa_bits()
        )

    def _prepare_multiplication(self, a: IEEENumber, b: IEEENumber):
        sign = a.get_sign() ^ b.get_sign()

        exp_a = self.bits.bits_to_int(a.get_exponent_bits())
        exp_b = self.bits.bits_to_int(b.get_exponent_bits())

        exponent = exp_a + exp_b - BIAS

        mant_a = [1] + a.get_mantissa_bits()
        mant_b = [1] + b.get_mantissa_bits()

        return sign, exponent, mant_a, mant_b

    def _multiply_mantissas(self, mant_a, mant_b):
        product = [0] * ((MANTISSA_LENGTH+1)*2)

        for i in range(MANTISSA_LENGTH + 1):
            if mant_b[MANTISSA_LENGTH - i] == 1:
                carry = 0
                for j in range(MANTISSA_LENGTH + 1):
                    idx = ((MANTISSA_LENGTH*2)-1) - (i + j)
                    sum = product[idx] + mant_a[MANTISSA_LENGTH - j] + carry
                    product[idx] = sum % 2
                    carry = sum // 2

                k = ((MANTISSA_LENGTH*2)-1) - (i + MANTISSA_LENGTH+1)
                while carry and k >= 0:
                    sum = product[k] + carry
                    product[k] = sum % 2
                    carry = sum // 2
                    k -= 1
        return product

    def _normalize_product(self, product, exponent):
        if product[0] == 1:
            mantissa_full = product[0:MANTISSA_LENGTH+2]
            rest = product[MANTISSA_LENGTH+2:]
            exponent += 1
        else:
            mantissa_full = product[1:MANTISSA_LENGTH+3]
            rest = product[MANTISSA_LENGTH+3:]

        return mantissa_full, rest, exponent

    def _round_mantissa(self, mantissa_full, rest, exponent):
        mantissa_24 = mantissa_full[:MANTISSA_LENGTH+1]
        extra_bit_for_rounding = mantissa_full[MANTISSA_LENGTH+1]
        sticky = 1 if any(rest) else 0

        if extra_bit_for_rounding == 1 and (sticky == 1 or mantissa_24[-1] == 1):
            carry = 1
            for i in range(MANTISSA_LENGTH, -1, -1):
                sum = mantissa_24[i] + carry
                mantissa_24[i] = sum % 2
                carry = sum // 2
            if carry == 1:
                mantissa_24 = [1] + mantissa_24[:-1]
                exponent += 1

        return mantissa_24, exponent

    def _build_result(self, sign, exponent, mantissa_24):
        if exponent >= EXP_MAX:
            return IEEENumber([sign] + [1]*EXP_BITS + [0]*MANTISSA_LENGTH)
        if exponent <= 0:
            return IEEENumber([0]*BITS_32)

        bits = [sign]
        bits += self.bits.int_to_bits(exponent, EXP_BITS)

        for i in range(MANTISSA_LENGTH):
            bits.append(mantissa_24[i + 1])

        return IEEENumber(bits)

    def multiply(self, a: IEEENumber, b: IEEENumber) -> IEEENumber:
        if self.is_nan(a) or self.is_nan(b):
            return IEEENumber([0] + [1]*EXP_BITS + [1] + [0]*(MANTISSA_LENGTH-1))
        if self.is_zero(a) or self.is_zero(b):
            return IEEENumber([0] * BITS_32)

        sign, exponent, mant_a, mant_b = self._prepare_multiplication(a, b)

        product = self._multiply_mantissas(mant_a, mant_b)

        mantissa_full, rest, exponent = self._normalize_product(product, exponent)
        mantissa_24, exponent = self._round_mantissa(mantissa_full, rest, exponent)

        return self._build_result(sign, exponent, mantissa_24)

    def get_mantissa_with_hidden(self, num: IEEENumber):
        mant = [0] * BITS_32
        mant[EXP_BITS] = 1

        src = num.get_mantissa_bits()
        for i in range(MANTISSA_LENGTH ):
            mant[EXP_BITS+1 + i] = src[i]

        return mant

    def mantissa_bits_to_int(self, mantissa_bits):
        value = 1 << MANTISSA_LENGTH

        for i in range(MANTISSA_LENGTH):
            if mantissa_bits[i] == 1:
                value |= 1 << ((MANTISSA_LENGTH-1) - i)

        return value

    def div_mantissas(self, mantis_A, mantis_B):
        if mantis_B == 0:
            raise ZeroDivisionError()

        quotient = (mantis_A << MANTISSA_LENGTH) // mantis_B

        shift = 0

        if quotient >= (1 << (MANTISSA_LENGTH+1)):
            quotient >>= 1
            shift = 1
        elif quotient < (1 << MANTISSA_LENGTH):
            while quotient < (1 << MANTISSA_LENGTH):
                quotient <<= 1
                shift -= 1

        return quotient, shift

    def divide(self, a: IEEENumber, b: IEEENumber) -> IEEENumber:
        if self.is_nan(a) or self.is_nan(b):
            return IEEENumber([0] + [1]*EXP_BITS + [1] + [0]*(MANTISSA_LENGTH-1))
        if self.is_infinity(a) and not self.is_infinity(b):
            return a.copy()  
        if self.is_zero(a) and self.is_zero(b):
            return IEEENumber([0] + [1] * EXP_BITS + [1] + [0] * (MANTISSA_LENGTH-1))
        if self.is_zero(b):
            sign = a.get_sign() ^ b.get_sign()
            return IEEENumber([sign] + [1] * EXP_BITS + [0] * (MANTISSA_LENGTH))
        if self.is_zero(a):
            return IEEENumber([0] * BITS_32)

        sign = a.get_sign() ^ b.get_sign()

        exp = (
            self.bits.bits_to_int(a.get_exponent_bits())
            - self.bits.bits_to_int(b.get_exponent_bits())
            + BIAS
        )

        mA = self.mantissa_bits_to_int(a.get_mantissa_bits())
        mB = self.mantissa_bits_to_int(b.get_mantissa_bits())

        mant_int, shift = self.div_mantissas(mA, mB)
        exp += shift

        if exp <= 0:
            return IEEENumber([0] * BITS_32)
        if exp >= EXP_MAX:
            return IEEENumber([sign] + [1] * EXP_BITS + [0] * MANTISSA_LENGTH)

        mantissa_bits = []
        for i in range(23):
            mantissa_bits.append((mant_int >> ((MANTISSA_LENGTH-1)- i)) & 1)

        return IEEENumber([sign] + self.bits.int_to_bits(exp, EXP_BITS) + mantissa_bits)
