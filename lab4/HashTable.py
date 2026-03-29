from typing import Any, Optional

try:
    from .KeyValueCalculator import KeyValueCalculator
    from .TableEntry import TableEntry
except ImportError:  # fallback for direct execution
    from KeyValueCalculator import KeyValueCalculator
    from TableEntry import TableEntry


class HashTable:
    DEFAULT_SIZE = 20

    def __init__(self, size: int = DEFAULT_SIZE, base_address: int = 0) -> None:
        if not isinstance(size, int) or size <= 0:
            raise ValueError("Size must be a positive integer.")
        self._table_size = size
        self._base_address = base_address
        self._slots: list[Optional[TableEntry]] = [None] * size
        self._active_count = 0
        self._key_calculator = KeyValueCalculator()

    @property
    def size(self) -> int:
        return self._table_size

    @property
    def base_address(self) -> int:
        return self._base_address

    def __len__(self) -> int:
        return self._active_count

    def load_factor(self) -> float:
        return self._active_count / self._table_size

    def calculate_value(self, identifier: str) -> int:
        return self._key_calculator.key_to_value(identifier)

    def calculate_address(self, identifier: str) -> int:
        return self._key_calculator.hash_address(
            identifier, self._table_size, self._base_address
        )

    def insert(self, identifier: str, payload: Any) -> None:
        if self._active_count >= self._table_size:
            raise OverflowError("Hash table is full.")

        base_address = self.calculate_address(identifier)
        first_deleted_index: Optional[int] = None
        first_deleted_step: Optional[int] = None

        for probe_step in range(self._table_size):
            probe_index = (base_address + probe_step * probe_step) % self._table_size
            slot_entry = self._slots[probe_index]

            if slot_entry is None:
                if first_deleted_index is not None:
                    self._write_entry(
                        first_deleted_index,
                        identifier,
                        payload,
                        base_address,
                        first_deleted_step or 0,
                    )
                else:
                    self._write_entry(
                        probe_index, identifier, payload, base_address, probe_step
                    )
                return

            if slot_entry.is_deleted == 1:
                if first_deleted_index is None:
                    first_deleted_index = probe_index
                    first_deleted_step = probe_step
                continue

            if slot_entry.identifier == identifier:
                raise KeyError("Key already exists.")

        if first_deleted_index is not None:
            self._write_entry(
                first_deleted_index,
                identifier,
                payload,
                base_address,
                first_deleted_step or 0,
            )
            return

        raise OverflowError("No free slot found for insertion.")

    def get(self, identifier: str) -> Any:
        slot_index = self._find_index(identifier)
        if slot_index is None:
            raise KeyError("Key not found.")
        slot_entry = self._slots[slot_index]
        if slot_entry is None or slot_entry.is_deleted == 1:
            raise KeyError("Key not found.")
        return slot_entry.payload

    def update(self, identifier: str, payload: Any) -> None:
        slot_index = self._find_index(identifier)
        if slot_index is None:
            raise KeyError("Key not found.")
        slot_entry = self._slots[slot_index]
        if slot_entry is None or slot_entry.is_deleted == 1:
            raise KeyError("Key not found.")
        slot_entry.payload = payload

    def delete(self, identifier: str) -> None:
        slot_index = self._find_index(identifier)
        if slot_index is None:
            raise KeyError("Key not found.")
        slot_entry = self._slots[slot_index]
        if slot_entry is None or slot_entry.is_deleted == 1:
            raise KeyError("Key not found.")
        slot_entry.is_deleted = 1
        slot_entry.is_occupied = 0
        self._active_count -= 1

    def contains(self, identifier: str) -> bool:
        try:
            self.get(identifier)
        except KeyError:
            return False
        return True

    def rows(self) -> list[tuple[int, Optional[TableEntry]]]:
        return list(enumerate(self._slots))

    def _find_index(self, identifier: str) -> Optional[int]:
        base_address = self.calculate_address(identifier)
        for probe_step in range(self._table_size):
            probe_index = (base_address + probe_step * probe_step) % self._table_size
            slot_entry = self._slots[probe_index]
            if slot_entry is None:
                return None
            if slot_entry.is_deleted == 1:
                continue
            if slot_entry.identifier == identifier:
                return probe_index
        return None

    def _write_entry(
        self,
        slot_index: int,
        identifier: str,
        payload: Any,
        base_address: int,
        probe_step: int,
    ) -> None:
        has_collision = 1 if probe_step > 0 else 0
        self._slots[slot_index] = TableEntry(
            identifier=identifier,
            payload=payload,
            has_collision=has_collision,
            is_occupied=1,
            is_deleted=0,
        )
        self._active_count += 1
