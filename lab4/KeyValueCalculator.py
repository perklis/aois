class KeyValueCalculator:
    ALPHABET_RU = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ"
    ALPHABET_EN = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    def key_to_value(self, key: str) -> int:
        if not isinstance(key, str):
            raise TypeError("Key must be a string.")
        key_text = key.strip()
        if not key_text:
            raise ValueError("Key must be non-empty.")

        first_char = key_text[0].upper()
        alphabet = self._pick_alphabet(first_char)
        alphabet_size = len(alphabet)

        second_char = key_text[1].upper() if len(key_text) > 1 else first_char

        try:
            first_index = alphabet.index(first_char)
            second_index = alphabet.index(second_char)
        except ValueError as exc:
            raise ValueError("Key must use one alphabet (RU or EN).") from exc

        return first_index * alphabet_size + second_index

    def hash_address(self, key: str, table_size: int, base_address: int = 0) -> int:
        if table_size <= 0:
            raise ValueError("Table size must be positive.")
        numeric_value = self.key_to_value(key)
        return (numeric_value % table_size) + base_address

    def _pick_alphabet(self, leading_char: str) -> str:
        if leading_char in self.ALPHABET_RU:
            return self.ALPHABET_RU
        if leading_char in self.ALPHABET_EN:
            return self.ALPHABET_EN
        raise ValueError("Key must start with a Russian or Latin letter.")
