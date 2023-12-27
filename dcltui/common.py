from typing import Callable
from functools import wraps
from .constants import *
from os import terminal_size
from .dcl_types import Element, Coords, Component, Renderer
from .renderer import renderer
from sys import stdout
from time import sleep
from pynput import keyboard
from .text_utils import right_pad, write


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


def double_lined_box_component(
    transform: Callable[[terminal_size], tuple[tuple[int, int], tuple[int, int]]]
) -> Component:
    def component(term_size: terminal_size, z_idx: int) -> Element:
        size, start_coords = transform(term_size)
        cols, lines = size

        fcols = cols - 2
        flines = lines - 2

        hfill = d_horizontal * fcols

        mid_line = f"{d_vertical}{' '*fcols}{d_vertical}"
        midlines = "\n".join([mid_line] * flines)

        out = f"""\
{d_top_left}{hfill}{d_top_right}
{midlines}
{d_bottom_left}{hfill}{d_bottom_right}
"""
        return (out, start_coords)

    return component


def text_input(
    start_pos: Coords, prefix: str, length: int, enter_handle: Callable[[str], None]
) -> Component:
    """
    Not really a component, it will live on its own thread and render.
    """
    start = f"\x1B[{start_pos[1]+1};{start_pos[0]+1}H"
    write(f"{start}{right_pad(prefix, length)}", True)
    postpref = f"\x1B[{start_pos[1]+1};{start_pos[0]+1+len(prefix)}H"
    pl = len(prefix)

    def closure(ts: terminal_size, z_idx: int) -> tuple[str, Coords]:
        return (prefix + right_pad(closure.text, length - pl), start_pos)

    closure.text = ""

    def on_key(key: keyboard.Key | keyboard.KeyCode | None) -> None:
        if isinstance(key, keyboard.KeyCode):
            closure.text += key.char
        elif key == keyboard.Key.space:
            closure.text += " "
        elif key == keyboard.Key.backspace:
            closure.text = closure.text[:-1]
        elif key == keyboard.Key.enter:
            enter_handle(closure.text)
            closure.text = ""
        write(f"{postpref}{right_pad(closure.text, length-pl)}", True)

    listener = keyboard.Listener(on_press=on_key)
    listener.start()

    return closure


def wrap(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
            done()
        except KeyboardInterrupt:
            write("\x1Bc", True)

    return wrapper


def done():
    while True:
        sleep(600)
