from typing import Any, Optional

from KeyValueCalculator import KeyValueCalculator
from TableEntry import TableEntry


class HashTable:
    DEFAULT_SIZE = 20

    def __init__(self, size: int = DEFAULT_SIZE, base_address: int = 0) -> None:
        if not isinstance(size, int) or size <= 0:
            raise ValueError("Size must be a positive integer.")
        self._size = size
        self._base_address = base_address
        self._table: list[Optional[TableEntry]] = [None] * size
        self._count = 0
        self._calc = KeyValueCalculator()

    @property
    def size(self) -> int:
        return self._size

    @property
    def base_address(self) -> int:
        return self._base_address

    def __len__(self) -> int:
        return self._count

    def load_factor(self) -> float:
        return self._count / self._size

    def calculate_v(self, key: str) -> int:
        return self._calc.key_to_value(key)

    def calculate_h(self, key: str) -> int:
        return self._calc.hash_address(key, self._size, self._base_address)

    def insert(self, key: str, value: Any) -> None:
        if self._count >= self._size:
            raise OverflowError("Hash table is full.")

        base_hash = self.calculate_h(key)
        first_deleted: Optional[int] = None
        first_deleted_step: Optional[int] = None

        for step in range(self._size):
            idx = (base_hash + step * step) % self._size
            entry = self._table[idx]

            if entry is None:
                if first_deleted is not None:
                    self._place_entry(
                        first_deleted, key, value, base_hash, first_deleted_step or 0
                    )
                else:
                    self._place_entry(idx, key, value, base_hash, step)
                return

            if entry.deleted_flag == 1:
                if first_deleted is None:
                    first_deleted = idx
                    first_deleted_step = step
                continue

            if entry.key == key:
                raise KeyError("Key already exists.")

        if first_deleted is not None:
            self._place_entry(
                first_deleted, key, value, base_hash, first_deleted_step or 0
            )
            return

        raise OverflowError("No free slot found for insertion.")

    def get(self, key: str) -> Any:
        idx = self._find_slot(key)
        if idx is None:
            raise KeyError("Key not found.")
        entry = self._table[idx]
        if entry is None or entry.deleted_flag == 1:
            raise KeyError("Key not found.")
        return entry.value

    def update(self, key: str, value: Any) -> None:
        idx = self._find_slot(key)
        if idx is None:
            raise KeyError("Key not found.")
        entry = self._table[idx]
        if entry is None or entry.deleted_flag == 1:
            raise KeyError("Key not found.")
        entry.value = value

    def delete(self, key: str) -> None:
        idx = self._find_slot(key)
        if idx is None:
            raise KeyError("Key not found.")
        entry = self._table[idx]
        if entry is None or entry.deleted_flag == 1:
            raise KeyError("Key not found.")
    
        entry.deleted_flag = 1
        entry.occupied_flag = 0
        self._count -= 1

    def contains(self, key: str) -> bool:
        try:
            self.get(key)
        except KeyError:
            return False
        return True

    def rows(self) -> list[tuple[int, Optional[TableEntry]]]:
        return list(enumerate(self._table))

    def _find_slot(self, key: str) -> Optional[int]:
        base_hash = self.calculate_h(key)
        for step in range(self._size):
            idx = (base_hash + step * step) % self._size
            entry = self._table[idx]
            if entry is None:
                return None
            if entry.deleted_flag == 1:
                continue
            if entry.key == key:
                return idx
        return None

    def _place_entry(self, idx: int, key: str, value: Any, base_hash: int, step: int) -> None:
        collision_flag = 1 if step > 0 else 0

        self._table[idx] = TableEntry(
            key=key,
            value=value,
            collision_flag=collision_flag,
            occupied_flag=1,
            deleted_flag=0,
        )
        self._count += 1
