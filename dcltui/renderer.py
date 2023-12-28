from __future__ import annotations

from typing import Iterable
from os import get_terminal_size, terminal_size

from .dcl_types import Component, Renderer, Coords
from .text_utils import write


def render(text: str, cords: Coords) -> None:
    start_x, start_y = cords
    for line_idx, line in enumerate(text.splitlines()):
        write(f"\x1B[{line_idx+start_y+1};{start_x+1}H{line}")


def renderer(
    components: Iterable[Component],
) -> Renderer:
    def closure(clear: bool = False) -> None:
        term_size: terminal_size = get_terminal_size()

        if clear is True:
            write("\x1Bc")

        for z_idx, component in enumerate(components):
            text, cords = component(term_size, z_idx)
            render(text, cords)

        write(
            f"\x1B[{term_size.lines+1};{term_size.columns+1}H", True
        )  # to not cause weird cursor positions + hide cursor

    return closure
