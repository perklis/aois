import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import qm


class TestQM(unittest.TestCase):
    def test_implicant_is_equal(self):
        a = qm.Implicant(1, 2)
        b = qm.Implicant(1, 2)
        c = qm.Implicant(2, 2)
        self.assertTrue(a.is_equal(b))
        self.assertFalse(a.is_equal(c))

    def test_differ_by_one_bit(self):
        a = qm.Implicant(0, 0)
        b = qm.Implicant(1, 0)
        ok, merged = qm.differ_by_one_bit(a, b)
        self.assertTrue(ok)
        self.assertEqual(merged.value, 0)
        self.assertEqual(merged.mask, 1)

        c = qm.Implicant(3, 0)
        ok, _ = qm.differ_by_one_bit(a, c)
        self.assertFalse(ok)

        d = qm.Implicant(0, 1)
        ok, _ = qm.differ_by_one_bit(a, d)
        self.assertFalse(ok)

    def test_implicant_covers(self):
        imp = qm.Implicant(0b10, 0b01)
        self.assertTrue(imp.covers(0b10))
        self.assertTrue(imp.covers(0b11))
        self.assertFalse(imp.covers(0b00))
        self.assertFalse(imp.covers(0b01))

    def test_generate_sdnf(self):
        res = qm.generate_sdnf(2, [1, 3], ["A", "B"])
        self.assertEqual(res, "(!A & B) | (A & B)")
        self.assertEqual(qm.generate_sdnf(2, [], ["A", "B"]), "0")

    def test_minimize(self):
        self.assertEqual(qm.minimize(2, [0, 1, 2, 3], None, ["A", "B"]), "1")
        self.assertEqual(qm.minimize(2, [], None, ["A", "B"]), "0")

        res = qm.minimize(3, [0, 1, 2, 5, 6, 7], [3], ["A", "B", "C"])
        self.assertTrue(len(res) > 0)

        res2 = qm.minimize(
            4,
            [0, 1, 2, 5, 6, 7, 8, 9, 10, 14],
            None,
            ["A", "B", "C", "D"],
        )
        self.assertTrue(len(res2) > 0)

    def test_minimize_simple(self):
        res = qm.minimize(2, [1, 3], None, ["A", "B"])
        self.assertEqual(res, "(B)")

    def test_minimize_with_dont_cares(self):
        res = qm.minimize(2, [1], [0], ["A", "B"])
        self.assertEqual(res, "(!A)")

    def test_internal_helpers(self):
        primes = qm._find_prime_implicants([0, 1], [])
        self.assertEqual(len(primes), 1)
        self.assertIn(qm.Implicant(0, 1), primes)

        primes = [
            qm.Implicant(0, 1),
            qm.Implicant(2, 1),
            qm.Implicant(0, 0),
        ]
        essentials, remaining = qm._find_essential_primes(primes, [0, 2])
        self.assertEqual(len(essentials), 1)
        self.assertEqual(essentials[0], qm.Implicant(2, 1))
        self.assertEqual(remaining, [0])

        solution = qm._cover_remaining([0, 2], primes, [])
        self.assertTrue(self._covers_all(solution, [0, 2]))

        best = qm._find_best_prime(primes[:2], [0, 1, 2])
        self.assertEqual(best.mask, 1)

        vars_ = ["A", "B"]
        self.assertEqual(qm._format_implicant(qm.Implicant(0, 0), 2, vars_), "(!A & !B)")
        self.assertEqual(
            qm._format_solution([qm.Implicant(0, 0), qm.Implicant(1, 0)], 2, vars_),
            "(!A & !B) | (!A & B)",
        )

    @staticmethod
    def _covers_all(solution, minterms):
        for m in minterms:
            if not any(imp.covers(m) for imp in solution):
                return False
        return True
