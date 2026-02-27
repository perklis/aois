class BitOperations:

    def int_to_bits(self, value, size):
        bits = [0] * size
        for i in range(size - 1, -1, -1):
            bits[i] = value % 2
            value //= 2
        return bits

    def bits_to_int(self, bits):
        value = 0
        for b in bits:
            value = value * 2 + b
        return value

    def add_bits(self, a, b):
        result = [0] * len(a)
        carry = 0
        for i in range(len(a) - 1, -1, -1):
            sum = a[i] + b[i] + carry
            result[i] = sum % 2
            carry = sum // 2
        return result, carry

    def subtract_bits(self, a, b):
        max_len = max(len(a), len(b))
        a = [0] * (max_len - len(a)) + a
        b = [0] * (max_len - len(b)) + b

        result = [0] * max_len
        borrow = 0
        for i in range(max_len - 1, -1, -1):
            sum = a[i] - b[i] - borrow
            if sum < 0:
                sum += 2
                borrow = 1
            else:
                borrow = 0
            result[i] = sum

        return result

    def compare_register(self, a, b):
        for i in range(len(a)):
            if a[i] > b[i]:
                return 1
            if a[i] < b[i]:
                return -1
        return 0

    def move_left(self, bits, count=1):
        for _ in range(count):
            for i in range(len(bits) - 1):
                bits[i] = bits[i + 1]
            bits[-1] = 0

    def move_right(self, bits, count=1):
        for _ in range(count):
            for i in range(len(bits) - 1, 0, -1):
                bits[i] = bits[i - 1]
            bits[0] = 0

    def sub_register(self, a, b):
        result = a[:]
        borrow = 0
        for i in range(len(a) - 1, -1, -1):
            step_result = result[i] - b[i] - borrow
            if step_result < 0:
                step_result += 2
                borrow = 1
            else:
                borrow = 0
            result[i] = step_result
        return result