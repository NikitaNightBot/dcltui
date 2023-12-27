from typing import Callable
from .constants import *
from os import terminal_size
from .dcl_types import Element, Coords, Component, Renderer
from .renderer import renderer


def cols_lines(size: terminal_size) -> Coords:  # columns, lines
    return (size.columns, size.lines)


def double_lined_full_component(term_size: terminal_size, z_idx: int) -> Element:
    cols, lines = cols_lines(term_size)

    fcols = cols - 2
    flines = lines - 2

    hfill = d_horizontal * fcols

    mid_line = f"{d_vertical}{' '*fcols}{d_vertical}"
    midlines = "\n".join([mid_line] * flines)

    out = f"""\
{d_top_left}{hfill}{d_top_right}
{midlines}
{d_bottom_left}{hfill}{d_bottom_right}"""

    return (out, HOME)

def double_lined_full_renderer() -> Renderer:
    return renderer([double_lined_full_component])

def double_lined_box_component(transform: Callable[[terminal_size], tuple[tuple[int, int], tuple[int, int]]]) -> Component:
    def component(term_size: terminal_size, z_idx: int) -> Element:
        size, start_coords = transform(term_size)
        cols, lines = size

        fcols = cols - 2
        flines = lines - 2

        hfill = d_horizontal * fcols

        mid_line = f"{d_vertical}{' '*fcols}{d_vertical}"
        midlines = "\n".join([mid_line]*flines)

        out = f"""\
{d_top_left}{hfill}{d_top_right}
{midlines}
{d_bottom_left}{hfill}{d_bottom_right}
"""
        return (out, start_coords)
    return component