class Implicant:
    def __init__(self, pattern, minterms):
        self.pattern = pattern
        self.minterms = tuple(sorted(minterms))

    def key(self):
        return self.pattern
