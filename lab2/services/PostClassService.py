from services.ZhegalkinPolinom import ZhegalkinPolinom


class PostClassService:
    def __init__(self):
        self.zhegalkin = ZhegalkinPolinom()

    def analyze(self, rows, variable_names):
        values = tuple(row.value for row in rows)
        return {
            "T0": values[0] == 0,
            "T1": values[-1] == 1,
            "S": self._is_self_dual(values, len(variable_names)),
            "M": self._is_monotone(values, len(variable_names)),
            "L": self.zhegalkin.max_degree(rows, variable_names) <= 1,
        }

    def _is_self_dual(self, values, variable_count):
        max_index = (1 << variable_count) - 1
        for index in range(len(values)):
            opposite = index ^ max_index
            if values[index] == values[opposite]:
                return False
        return True

    def _is_monotone(self, values, variable_count):
        for left in range(len(values)):
            for right in range(len(values)):
                if not self._dominates(left, right, variable_count):
                    continue
                if values[left] > values[right]:
                    return False
        return True

    def _dominates(self, left, right, variable_count):
        for shift in range(variable_count):
            left_bit = (left >> shift) & 1
            right_bit = (right >> shift) & 1
            if left_bit > right_bit:
                return False
        return True
