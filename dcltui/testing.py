from __future__ import annotations

from typing import Callable, TypeAlias
from os import get_terminal_size, terminal_size
from sys import stdout

# https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
HOME: tuple[int, int] = (0, 0)
# https://en.wikipedia.org/wiki/Box-drawing_character
d_horizontal = chr(0x2550)
d_vertical = chr(0x2551)
d_right_vertical = chr(0x255E)
d_left_vertical = chr(0x2561)
d_down_horizontal = chr(0x2565)
d_up_d_horizontal = chr(0x2569)
d_top_left = chr(0x2554)
d_top_right = chr(0x2557)
d_bottom_left = chr(0x255A)
d_bottom_right = chr(0x255D)
d_left_d_vertical = chr(0x2563)
d_right_d_vertical = chr(0x2560)
d_down_d_horizontal = chr(0x2566)


def col_lines(size: terminal_size) -> tuple[int, int]:  # columns, lines
    return (size.columns, size.lines)


def write(
    text: str,
    flush: bool = False,
    w=stdout.write,
    f=stdout.flush,  # local names faster lookup
) -> None:
    w(text)
    if flush:
        f()


Component: TypeAlias = Callable[
    [terminal_size, int],  # size on render, render (z) idx
    tuple[
        str,  # want to feature some sort of custom template strings later
        tuple[int, int],  # start coordinates
    ],
]


def renderer(
    components: list[Component],
) -> Callable[[bool], None]:
    def closure(clear: bool = True) -> None:
        term_size: terminal_size = get_terminal_size()

        if clear is True:
            write("\x1Bc")

        for z_idx, component in enumerate(components):
            text, (start_x, start_y) = component(term_size, z_idx)
            for line_idx, line in enumerate(text.splitlines()):
                write(f"\x1B[{line_idx+start_y+1};{start_x+1}H{line}")

        write(
            f"\x1B[{term_size.lines+1};{term_size.columns+1}H", True
        )  # to not cause weird cursor positions + hide cursor

    return closure


def main() -> None:
    def layout(term_size: terminal_size, z_idx: int) -> tuple[str, tuple[int, int]]:
        columns, lines = col_lines(term_size)
        flines = lines - 2
        fcols = columns - 2
        midline = f"{d_vertical}{' '*(fcols)}{d_vertical}"
        midlines = "\n".join([midline] * flines)

        out = f"""\
{d_top_left}{d_horizontal*fcols}{d_top_right}
{midlines}
{d_bottom_left}{d_horizontal*fcols}{d_bottom_right}"""
        return (out, HOME)

    render = renderer([layout])

    render()
    input()


if __name__ == "__main__":
    main()
