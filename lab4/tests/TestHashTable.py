import unittest

from HashTable import HashTable


class TestHashTable(unittest.TestCase):
    def test_insert_get(self):
        table = HashTable(size=5)
        table.insert("AA", "first")
        self.assertEqual(table.get("AA"), "first")
        self.assertEqual(len(table), 1)

    def test_quadratic_probing_collision(self):
        table = HashTable(size=5)
        table.insert("AA", "v1")
        table.insert("BA", "v2")
        self.assertEqual(table.get("AA"), "v1")
        self.assertEqual(table.get("BA"), "v2")

    def test_update(self):
        table = HashTable(size=5)
        table.insert("AA", "v1")
        table.update("AA", "v2")
        self.assertEqual(table.get("AA"), "v2")

    def test_delete_and_reuse_slot(self):
        table = HashTable(size=5)
        table.insert("AA", "v1")
        table.insert("FA", "v2")
        table.insert("KA", "v3")
        table.delete("FA")
        self.assertEqual(len(table), 2)
        table.insert("PA", "v4")
        self.assertTrue(table.contains("PA"))
        self.assertEqual(len(table), 3)

    def test_duplicate_insert_raises(self):
        table = HashTable(size=5)
        table.insert("AA", "v1")
        with self.assertRaises(KeyError):
            table.insert("AA", "v2")

    def test_delete_missing_key_raises(self):
        table = HashTable(size=5)
        with self.assertRaises(KeyError):
            table.delete("AA")

    def test_full_table_raises(self):
        table = HashTable(size=2)
        table.insert("AA", "v1")
        table.insert("BA", "v2")
        with self.assertRaises(OverflowError):
            table.insert("CA", "v3")

    def test_load_factor(self):
        table = HashTable(size=4)
        table.insert("AA", "v1")
        table.insert("BA", "v2")
        self.assertAlmostEqual(table.load_factor(), 0.5)


