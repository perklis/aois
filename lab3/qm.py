from __future__ import annotations

from typing import Iterable, List, Tuple

from Implicant import Implicant


def differ_by_one_bit(a: Implicant, b: Implicant) -> Tuple[bool, Implicant]:
    if a.mask != b.mask:
        return False, Implicant(0, 0)
    diff = a.value ^ b.value
    if diff != 0 and (diff & (diff - 1)) == 0:
        merged = Implicant(value=a.value & ~diff, mask=a.mask | diff)
        return True, merged
    return False, Implicant(0, 0)


def generate_sdnf(num_vars: int, minterms: Iterable[int], var_names: List[str]) -> str:
    minterms_list = list(minterms)
    if not minterms_list:
        return "0"
    parts = [
        _format_implicant(Implicant(value=m, mask=0), num_vars, var_names)
        for m in minterms_list
    ]
    return " | ".join(parts)


def minimize(
    num_vars: int,
    minterms: Iterable[int],
    dont_cares: Iterable[int] | None,
    var_names: List[str],
) -> str:
    minterms_list = list(minterms)
    if not minterms_list:
        return "0"
    dont_cares_list = list(dont_cares or [])
    primes = _find_prime_implicants(minterms_list, dont_cares_list)
    essentials, remaining = _find_essential_primes(primes, minterms_list)
    solution = _cover_remaining(remaining, primes, essentials)
    return _format_solution(solution, num_vars, var_names)


def _find_prime_implicants(minterms: List[int], dont_cares: List[int]) -> List[Implicant]:
    implicants = _init_implicants(minterms, dont_cares)
    primes: dict[Implicant, bool] = {}

    while implicants:
        next_level: dict[Implicant, bool] = {}
        used: dict[Implicant, bool] = {}

        for i, a in enumerate(implicants):
            for j in range(i + 1, len(implicants)):
                b = implicants[j]
                can_merge, merged = differ_by_one_bit(a, b)
                if can_merge:
                    next_level[merged] = True
                    used[a] = True
                    used[b] = True

        for imp in implicants:
            if not used.get(imp, False):
                primes[imp] = True

        implicants = list(next_level.keys())

    return list(primes.keys())


def _init_implicants(minterms: List[int], dont_cares: List[int]) -> List[Implicant]:
    res = [Implicant(value=m, mask=0) for m in minterms]
    res.extend(Implicant(value=m, mask=0) for m in dont_cares)
    return res


def _find_essential_primes(
    primes: List[Implicant], minterms: List[int]
) -> Tuple[List[Implicant], List[int]]:
    essentials: List[Implicant] = []
    covered: dict[int, bool] = {}

    for m in minterms:
        covers = _get_covers(primes, m)
        if len(covers) == 1:
            essentials = _append_unique(essentials, covers[0])

    for e in essentials:
        for m in minterms:
            if e.covers(m):
                covered[m] = True

    remaining = [m for m in minterms if not covered.get(m, False)]
    return essentials, remaining


def _get_covers(primes: List[Implicant], minterm: int) -> List[Implicant]:
    return [p for p in primes if p.covers(minterm)]


def _append_unique(items: List[Implicant], item: Implicant) -> List[Implicant]:
    if any(x.is_equal(item) for x in items):
        return items
    return items + [item]


def _cover_remaining(
    remaining: List[int],
    primes: List[Implicant],
    essentials: List[Implicant],
) -> List[Implicant]:
    solution = list(essentials)
    uncovered = list(remaining)

    while uncovered:
        best = _find_best_prime(primes, uncovered)
        solution.append(best)
        uncovered = [m for m in uncovered if not best.covers(m)]

    return solution


def _find_best_prime(primes: List[Implicant], uncovered: List[int]) -> Implicant:
    best_count = -1
    best = primes[0]
    for p in primes:
        count = sum(1 for m in uncovered if p.covers(m))
        if count > best_count:
            best_count = count
            best = p
    return best


def _format_solution(solution: List[Implicant], num_vars: int, var_names: List[str]) -> str:
    parts: List[str] = []
    full_mask = (1 << num_vars) - 1
    for imp in solution:
        if imp.mask == full_mask:
            return "1"
        parts.append(_format_implicant(imp, num_vars, var_names))
    return " | ".join(parts)


def _format_implicant(imp: Implicant, num_vars: int, var_names: List[str]) -> str:
    parts: List[str] = []
    for i in range(num_vars):
        bit_pos = num_vars - 1 - i
        if ((imp.mask >> bit_pos) & 1) == 0:
            if ((imp.value >> bit_pos) & 1) == 1:
                parts.append(var_names[i])
            else:
                parts.append("!" + var_names[i])
    return "(" + " & ".join(parts) + ")"
