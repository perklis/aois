from dataclasses import dataclass


@dataclass(frozen=True)
class Implicant:
    value: int
    mask: int

    def is_equal(self, other: "Implicant") -> bool:
        return self.value == other.value and self.mask == other.mask

    def covers(self, minterm: int) -> bool:
        return (minterm & ~self.mask) == (self.value & ~self.mask)
