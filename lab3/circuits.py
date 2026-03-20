from __future__ import annotations

from typing import List, Tuple

import qm
from Equation import Equation
from constants import (
    CounterInputs,
    CounterMaxState,
    DecoderInputs,
    EncoderInputs,
    OFFSET_N,
    SubtractorInputs,
)


def get_subtractor_equations() -> List[Equation]:
    vars_ = ["X1", "X2", "X3"]
    d_minterms = [1, 2, 4, 7]
    b_minterms = [1, 2, 3, 7]

    return [
        Equation(
            name="d (Разность)",
            sdnf=qm.generate_sdnf(SubtractorInputs, d_minterms, vars_),
            minimized=qm.minimize(SubtractorInputs, d_minterms, None, vars_),
        ),
        Equation(
            name="b (Заем)",
            sdnf=qm.generate_sdnf(SubtractorInputs, b_minterms, vars_),
            minimized=qm.minimize(SubtractorInputs, b_minterms, None, vars_),
        ),
    ]


def decode_8421(v: int) -> Tuple[int, bool]:
    if 0 <= v <= 9:
        return v, True
    return -1, False


def encode_8421(v: int) -> int:
    if 0 <= v <= 9:
        return v
    return 0


def get_decoder_8421_equations() -> List[Equation]:
    vars_ = ["I3", "I2", "I1", "I0"]
    minterms: dict[str, List[int]] = {"O3": [], "O2": [], "O1": [], "O0": []}
    dont_cares: List[int] = []

    for i in range(16):
        val, ok = decode_8421(i)
        if not ok:
            dont_cares.append(i)
            continue
        if (val & 8) != 0:
            minterms["O3"].append(i)
        if (val & 4) != 0:
            minterms["O2"].append(i)
        if (val & 2) != 0:
            minterms["O1"].append(i)
        if (val & 1) != 0:
            minterms["O0"].append(i)

    out_names = ["O3", "O2", "O1", "O0"]
    result: List[Equation] = []
    for out in out_names:
        result.append(
            Equation(
                name=out,
                sdnf="",
                minimized=qm.minimize(DecoderInputs, minterms[out], dont_cares, vars_),
            )
        )
    return result


def get_encoder_8421_equations(offset_n: int) -> List[Equation]:
    vars_ = ["S4", "S3", "S2", "S1", "S0"]
    minterms: dict[str, List[int]] = {
        "T3": [],
        "T2": [],
        "T1": [],
        "T0": [],
        "U3": [],
        "U2": [],
        "U1": [],
        "U0": [],
    }
    dont_cares: List[int] = []

    max_sum = 18 + offset_n
    for i in range(max_sum + 1, 32):
        dont_cares.append(i)

    for i in range(max_sum + 1):
        tens = i // 10
        units = i % 10
        t_b = encode_8421(tens)
        u_b = encode_8421(units)

        if (t_b & 8) != 0:
            minterms["T3"].append(i)
        if (t_b & 4) != 0:
            minterms["T2"].append(i)
        if (t_b & 2) != 0:
            minterms["T1"].append(i)
        if (t_b & 1) != 0:
            minterms["T0"].append(i)

        if (u_b & 8) != 0:
            minterms["U3"].append(i)
        if (u_b & 4) != 0:
            minterms["U2"].append(i)
        if (u_b & 2) != 0:
            minterms["U1"].append(i)
        if (u_b & 1) != 0:
            minterms["U0"].append(i)

    out_names = ["T3", "T2", "T1", "T0", "U3", "U2", "U1", "U0"]
    result: List[Equation] = []
    for out in out_names:
        result.append(
            Equation(
                name=out,
                sdnf="",
                minimized=qm.minimize(EncoderInputs, minterms[out], dont_cares, vars_),
            )
        )
    return result


def get_encoder_8421_equations_offset_n() -> List[Equation]:
    return get_encoder_8421_equations(OFFSET_N)


def get_counter_equations() -> List[Equation]:
    vars_ = ["Q4", "Q3", "Q2", "Q1"]
    minterms: List[List[int]] = [[], [], [], []]

    for q in range(CounterMaxState):
        next_q = (q - 1 + CounterMaxState) % CounterMaxState
        t_vals = q ^ next_q
        for i in range(4):
            if ((t_vals >> (3 - i)) & 1) == 1:
                minterms[i].append(q)

    out_names = ["T4", "T3", "T2", "T1"]
    result: List[Equation] = []
    for i in range(4):
        result.append(
            Equation(
                name=out_names[i],
                sdnf="",
                minimized=qm.minimize(CounterInputs, minterms[i], None, vars_),
            )
        )
    return result
