import os
import re
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import circuits
import constants


def eval_expr(expr: str, mapping: dict) -> bool:
    expr = expr.strip()
    if expr == "1":
        return True
    if expr == "0" or expr == "":
        return False
    expr = expr.replace("!", " not ")
    expr = expr.replace("&", " and ")
    expr = expr.replace("|", " or ")
    tokens = set(re.findall(r"[A-Za-z_][A-Za-z0-9_]*", expr))
    for token in sorted(tokens, key=len, reverse=True):
        if token in {"and", "or", "not"}:
            continue
        expr = re.sub(rf"\b{token}\b", f"mapping['{token}']", expr)
    return bool(eval(expr, {"__builtins__": {}}, {"mapping": mapping}))


class TestCircuits(unittest.TestCase):
    def test_decode_encode_8421(self):
        for v in range(10):
            enc = circuits.encode_8421(v)
            self.assertEqual(enc, v)
            dec, ok = circuits.decode_8421(enc)
            self.assertTrue(ok)
            self.assertEqual(dec, v)

        for v in range(10, 16):
            dec, ok = circuits.decode_8421(v)
            self.assertFalse(ok)
            self.assertEqual(dec, -1)

        self.assertEqual(circuits.encode_8421(-1), 0)
        self.assertEqual(circuits.encode_8421(15), 0)

    def test_subtractor_equations(self):
        eqs = circuits.get_subtractor_equations()
        self.assertEqual(len(eqs), 2)
        self.assertTrue(eqs[0].sdnf)
        self.assertTrue(eqs[1].sdnf)

        d_minterms = {1, 2, 4, 7}
        b_minterms = {1, 2, 3, 7}
        names = {"d": d_minterms, "b": b_minterms}

        for eq in eqs:
            if eq.name.startswith("d"):
                expected = names["d"]
            else:
                expected = names["b"]
            for value in range(8):
                mapping = {
                    "X1": bool((value >> 2) & 1),
                    "X2": bool((value >> 1) & 1),
                    "X3": bool(value & 1),
                }
                got = eval_expr(eq.minimized, mapping)
                self.assertEqual(got, value in expected)

    def test_decoder_equations(self):
        eqs = circuits.get_decoder_8421_equations()
        self.assertEqual(len(eqs), 4)
        eq_map = {eq.name: eq.minimized for eq in eqs}

        for i in range(10):
            mapping = {
                "I3": bool((i >> 3) & 1),
                "I2": bool((i >> 2) & 1),
                "I1": bool((i >> 1) & 1),
                "I0": bool(i & 1),
            }
            for bit, name in enumerate(["O0", "O1", "O2", "O3"]):
                expected = bool((i >> bit) & 1)
                got = eval_expr(eq_map[name], mapping)
                self.assertEqual(got, expected)

    def _check_encoder(self, offset):
        eqs = circuits.get_encoder_8421_equations(offset)
        self.assertEqual(len(eqs), 8)
        eq_map = {eq.name: eq.minimized for eq in eqs}

        max_sum = 18 + offset
        for i in range(max_sum + 1):
            mapping = {
                "S4": bool((i >> 4) & 1),
                "S3": bool((i >> 3) & 1),
                "S2": bool((i >> 2) & 1),
                "S1": bool((i >> 1) & 1),
                "S0": bool(i & 1),
            }
            tens = i // 10
            units = i % 10
            t_b = circuits.encode_8421(tens)
            u_b = circuits.encode_8421(units)
            expected = {
                "T3": bool(t_b & 8),
                "T2": bool(t_b & 4),
                "T1": bool(t_b & 2),
                "T0": bool(t_b & 1),
                "U3": bool(u_b & 8),
                "U2": bool(u_b & 4),
                "U1": bool(u_b & 2),
                "U0": bool(u_b & 1),
            }
            for name, exp in expected.items():
                got = eval_expr(eq_map[name], mapping)
                self.assertEqual(got, exp)

    def test_encoder_equations_offset_n(self):
        self._check_encoder(constants.OFFSET_N)
        eqs = circuits.get_encoder_8421_equations_offset_n()
        self.assertEqual(len(eqs), 8)

    def test_counter_equations(self):
        eqs = circuits.get_counter_equations()
        self.assertEqual(len(eqs), 4)
        eq_map = {eq.name: eq.minimized for eq in eqs}

        for q in range(constants.CounterMaxState):
            mapping = {
                "Q4": bool((q >> 3) & 1),
                "Q3": bool((q >> 2) & 1),
                "Q2": bool((q >> 1) & 1),
                "Q1": bool(q & 1),
            }
            next_q = (q - 1 + constants.CounterMaxState) % constants.CounterMaxState
            t_vals = q ^ next_q
            expected = {
                "T4": bool((t_vals >> 3) & 1),
                "T3": bool((t_vals >> 2) & 1),
                "T2": bool((t_vals >> 1) & 1),
                "T1": bool(t_vals & 1),
            }
            for name, exp in expected.items():
                got = eval_expr(eq_map[name], mapping)
                self.assertEqual(got, exp)
