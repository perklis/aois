from __future__ import annotations

import circuits


def _print_equations(title: str, equations, show_sdnf: bool = False) -> None:
    print(title)
    for eq in equations:
        if show_sdnf:
            print(f"{eq.name}:\nSDNF: {eq.sdnf}\nMinimized: {eq.minimized}\n")
        else:
            print(f"{eq.name} = {eq.minimized}")
    print()


def main() -> None:
    _print_equations("Часть 1: ОДВ-3 (1-разрядный вычитатель)", circuits.get_subtractor_equations(), True)
    _print_equations("Часть 2.1: Декодер 8421 -> Двоичный", circuits.get_decoder_8421_equations())
    _print_equations(
        "Часть 2.2: Энкодер двоичный -> 8421 (смещение n=9)",
        circuits.get_encoder_8421_equations_offset_n(),
    )
    _print_equations("Часть 3: Вычитающий счётчик на 16 состояний (Т-триггер)", circuits.get_counter_equations())


if __name__ == "__main__":
    main()
