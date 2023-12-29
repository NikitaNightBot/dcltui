from .constants import (
    d_horizontal,
    d_vertical,
    d_top_left,
    d_top_right,
    d_bottom_left,
    d_bottom_right,
)
from os import terminal_size
from .dcl_types import Component


def d_box_fullscreen() -> Component:
    def closure(ts: terminal_size) -> tuple[str, tuple[int, int]]:
        col, lin = ts.columns, ts.lines
        fcol = col - 2
        flin = lin - 2
        hori = d_horizontal * fcol
        top = f"{d_top_left}{hori}{d_top_right}"
        mid = f"{d_vertical}{' '*fcol}{d_vertical}"
        mids = "\n".join([mid] * flin)
        bot = f"{d_bottom_left}{hori}{d_bottom_right}"
        return (f"{top}\n{mids}\n{bot}", (0, 0))

    return Component(
        lambda ts: (ts.columns, ts.lines),
        closure,
    )
