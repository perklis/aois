from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class TableEntry:
    identifier: str
    payload: Any
    has_collision: int  # C
    is_occupied: int  # U
    is_deleted: int  # D
