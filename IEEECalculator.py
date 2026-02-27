from IEEENumbers import IEEENumber
from BitOperations import BitOperations
from exceptions import ExponentOverflowError, ExponentUnderflowError

class IEEECalculator:
    BIAS = 127

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

    def _convert_integer_part(self, int_part_str):
        int_value = 0
        for c in int_part_str:
            int_value = int_value * 10 + int(c)
        if int_value == 0:
            return [0]

        bits = []
        while int_value > 0:
            bits.insert(0, int_value % 2)
            int_value //= 2

        return bits

    def _convert_fraction_part(self, frac_part_str):
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

        exponent += self.BIAS

        mantissa_bits = mantissa_bits[:23]
        while len(mantissa_bits) < 23:
            mantissa_bits.append(0)

        return exponent, mantissa_bits

    def _build_ieee_number(self, sign, exponent, mantissa_bits):
        exponent_bits = self.bits.int_to_bits(exponent, 8)
        return IEEENumber([sign] + exponent_bits + mantissa_bits)

    def decimal_to_ieee(self, number_str: str):
        number_str = number_str.strip().lower()

        if number_str in ("inf", "+inf", "INF", "+INF"):
            return IEEENumber([0] + [1]*8 + [0]*23)  
        if number_str in ("-inf", "-INF"):
            return IEEENumber([1] + [1]*8 + [0]*23) 
        if number_str in ("nan", "NaN", "NAN"):
            return IEEENumber([0] + [1]*8 + [1] + [0]*22) 


        sign, number_str = self._extract_sign(number_str)
        int_part_str, frac_part_str = self._split_parts(number_str)

        if self._is_zero(int_part_str, frac_part_str):
            return IEEENumber([sign] + [0] * 31)

        int_bits = self._convert_integer_part(int_part_str)
        frac_bits = self._convert_fraction_part(frac_part_str)
        exponent, mantissa_bits = self._build_normalized_parts(int_bits, frac_bits)

        return self._build_ieee_number(sign, exponent, mantissa_bits)

    def _prepare_addition(self, A: IEEENumber, B: IEEENumber):
        sign_a = A.get_sign()
        sign_b = B.get_sign()

        exp_a = self.bits.bits_to_int(A.get_exponent_bits())
        exp_b = self.bits.bits_to_int(B.get_exponent_bits())

        mant_a = self.get_mantissa_with_hidden(A)
        mant_b = self.get_mantissa_with_hidden(B)

        while len(mant_a) < 24:
            mant_a.append(0)
        while len(mant_b) < 24:
            mant_b.append(0)

        return sign_a, sign_b, exp_a, exp_b, mant_a, mant_b

    def _align_exponents(self, mant_a, mant_b, exp_a, exp_b):
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
            cmp = self.bits.compare_register(mant_a, mant_b)

            if cmp == 0:
                return None, 0, 0

            if cmp > 0:
                return self.bits.subtract_bits(mant_a, mant_b), sign_a, 0
            else:
                return self.bits.subtract_bits(mant_b, mant_a), sign_b, 0

    def _normalize_after_add(self, mant_res, exponent):
        if mant_res[7] == 1:
            self.bits.move_right(mant_res, 1)
            exponent += 1

        while mant_res[8] == 0 and exponent > 0:
            self.bits.move_left(mant_res, 1)
            exponent -= 1

        return mant_res, exponent

    def _build_add_result(self, sign_res, exponent, mant_res):
        if exponent >= 255:
            return IEEENumber([sign_res] + [1] * 8 + [0] * 23)

        if exponent <= 0:
            return IEEENumber([0] * 32)

        mantissa_bits = mant_res[9:32]
        exponent_bits = self.bits.int_to_bits(exponent, 8)

        return IEEENumber([sign_res] + exponent_bits + mantissa_bits)

    def is_nan(self, num: IEEENumber):
        exp = self.bits.bits_to_int(num.get_exponent_bits())
        mant = num.get_mantissa_bits()
        return exp == 255 and any(b == 1 for b in mant)

    def is_infinity(self, num: IEEENumber):
        exp = self.bits.bits_to_int(num.get_exponent_bits())
        mant = num.get_mantissa_bits()
        return exp == 255 and all(b == 0 for b in mant)

    def add(self, A: IEEENumber, B: IEEENumber):

        if self.is_nan(A) or self.is_nan(B):
            return IEEENumber([0] + [1]*8 + [1] + [0]*22)
    
        if self.is_infinity(A):
            if self.is_infinity(B) and A.get_sign() != B.get_sign():
                return IEEENumber([0] + [1]*8 + [1] + [0]*22)
            return A.copy()
        if self.is_infinity(B):
            return B.copy()
        if self.is_zero(A):
            return B.copy()
        if self.is_zero(B):
            return A.copy()

        sign_a, sign_b, exp_a, exp_b, mant_a, mant_b = self._prepare_addition(A, B)

        mant_a, mant_b, exponent = self._align_exponents(mant_a, mant_b, exp_a, exp_b)

        mant_res, sign_res, carry_shift = self._add_or_sub_mantissas(
            mant_a, mant_b, sign_a, sign_b
        )

        if mant_res is None:
            return IEEENumber([0] * 32)

        exponent += carry_shift
        mant_res, exponent = self._normalize_after_add(mant_res, exponent)

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

        exponent = exp_a + exp_b - self.BIAS

        mant_a = [1] + a.get_mantissa_bits()
        mant_b = [1] + b.get_mantissa_bits()

        return sign, exponent, mant_a, mant_b

    def _multiply_mantissas(self, mant_a, mant_b):
        product = [0] * 48

        for i in range(24):
            if mant_b[23 - i] == 1:
                carry = 0
                for j in range(24):
                    idx = 47 - (i + j)
                    s = product[idx] + mant_a[23 - j] + carry
                    product[idx] = s % 2
                    carry = s // 2

                k = 47 - (i + 24)
                while carry and k >= 0:
                    s = product[k] + carry
                    product[k] = s % 2
                    carry = s // 2
                    k -= 1

        return product

    def _normalize_product(self, product, exponent):
        if product[0] == 1:
            mantissa_full = product[0:25]
            rest = product[25:]
            exponent += 1
        else:
            mantissa_full = product[1:26]
            rest = product[26:]

        return mantissa_full, rest, exponent

    def _round_mantissa(self, mantissa_full, rest, exponent):
        mantissa_24 = mantissa_full[:24]
        guard = mantissa_full[24]
        sticky = 1 if any(rest) else 0

        if guard == 1 and (sticky == 1 or mantissa_24[-1] == 1):
            carry = 1
            for i in range(23, -1, -1):
                s = mantissa_24[i] + carry
                mantissa_24[i] = s % 2
                carry = s // 2
            if carry == 1:
                mantissa_24 = [1] + mantissa_24[:-1]
                exponent += 1

        return mantissa_24, exponent

    def _build_result(self, sign, exponent, mantissa_24):
        if exponent >= 255:
            raise ExponentOverflowError("Переполнение экспоненты")
        if exponent <= 0:
            raise ExponentUnderflowError("Переполнение экспоненты")

        bits = [sign]
        bits += self.bits.int_to_bits(exponent, 8)

        for i in range(23):
            bits.append(mantissa_24[i + 1])

        return IEEENumber(bits)

    def multiply(self, a: IEEENumber, b: IEEENumber) -> IEEENumber:
        if self.is_zero(a) or self.is_zero(b):
            return IEEENumber([0] * 32)

        sign, exponent, mant_a, mant_b = self._prepare_multiplication(a, b)

        product = self._multiply_mantissas(mant_a, mant_b)

        mantissa_full, rest, exponent = self._normalize_product(product, exponent)

        mantissa_24, exponent = self._round_mantissa(mantissa_full, rest, exponent)

        return self._build_result(sign, exponent, mantissa_24)

    def get_mantissa_with_hidden(self, num: IEEENumber):
        mant = [0] * 32
        mant[8] = 1

        src = num.get_mantissa_bits()
        for i in range(23):
            mant[9 + i] = src[i]

        return mant

    def mantissa_bits_to_int(self, mantissa_bits):
        value = 1 << 23

        for i in range(23):
            if mantissa_bits[i] == 1:
                value |= 1 << (22 - i)

        return value

    def div_mantissas(self, mA, mB):
        if mB == 0:
            raise ZeroDivisionError()

        quotient = (mA << 23) // mB

        shift = 0

        if quotient >= (1 << 24):
            quotient >>= 1
            shift = 1
        elif quotient < (1 << 23):
            while quotient < (1 << 23):
                quotient <<= 1
                shift -= 1

        return quotient, shift

    def divide(self, a: IEEENumber, b: IEEENumber) -> IEEENumber:
        if self.is_zero(a) and self.is_zero(b):
            return IEEENumber([0] + [1]*8 + [1] + [0]*22)
        if self.is_zero(b):
            sign = a.get_sign() ^ b.get_sign()
            return IEEENumber([sign] + [1]*8 + [0]*23)        
        if self.is_zero(a):
            return IEEENumber([0] * 32)

        sign = a.get_sign() ^ b.get_sign()

        exp = (
            self.bits.bits_to_int(a.get_exponent_bits())
            - self.bits.bits_to_int(b.get_exponent_bits())
            + self.BIAS
        )

        mA = self.mantissa_bits_to_int(a.get_mantissa_bits())
        mB = self.mantissa_bits_to_int(b.get_mantissa_bits())

        mant_int, shift = self.div_mantissas(mA, mB)
        exp += shift

        if exp <= 0:
            return IEEENumber([0] * 32)
        if exp >= 255:
            return IEEENumber([sign] + [1] * 8 + [0] * 23)

        mantissa_bits = []
        for i in range(23):
            mantissa_bits.append((mant_int >> (22 - i)) & 1)

        return IEEENumber([sign] + self.bits.int_to_bits(exp, 8) + mantissa_bits)
