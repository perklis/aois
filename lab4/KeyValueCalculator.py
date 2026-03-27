class KeyValueCalculator:
    ALPHABET_RU = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    ALPHABET_EN = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def key_to_value(self, key: str) -> int:
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")
        key = key.strip()
        if not key:
            raise ValueError("Key must be non-empty.")

        first = key[0].upper()
        alphabet = self._pick_alphabet(first)
        base = len(alphabet)

        second = key[1].upper() if len(key) > 1 else first

        try:
            a = alphabet.index(first)
            b = alphabet.index(second)
        except ValueError as exc:
            raise ValueError("Key must use one alphabet (RU or EN).") from exc

        return a * base + b

    def hash_address(self, key: str, table_size: int, base_address: int = 0) -> int:
        if table_size <= 0:
            raise ValueError("Table size must be positive.")
        v_value = self.key_to_value(key)
        return (v_value % table_size) + base_address

    def _pick_alphabet(self, first_char: str) -> str:
        if first_char in self.ALPHABET_RU:
            return self.ALPHABET_RU
        if first_char in self.ALPHABET_EN:
            return self.ALPHABET_EN
        raise ValueError("Key must start with a Russian or Latin letter.")
