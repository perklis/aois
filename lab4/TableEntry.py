from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class TableEntry:
    key: str
    value: Any
    collision_flag: int  # C
    occupied_flag: int  # U
    deleted_flag: int  # D
