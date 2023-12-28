from typing import Callable, Iterable, NoReturn
from os import get_terminal_size, terminal_size
from functools import wraps
from os import terminal_size
from time import sleep, perf_counter
from pynput import keyboard

from .constants import (
    HOME,
    d_horizontal,
    d_vertical,
    d_right_vertical,
    d_left_vertical,
    d_down_horizontal,
    d_up_d_horizontal,
    d_top_left,
    d_top_right,
    d_bottom_left,
    d_bottom_right,
    d_left_d_vertical,
    d_right_d_vertical,
    d_down_d_horizontal,
)
from .dcl_types import Element, Coords, Component, Renderer, Transform, TextInput
from .renderer import renderer
from .text_utils import right_pad, write
from threading import Thread


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


def double_lined_box_component(transform: Transform) -> Component:
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
    start_pos: Coords, prefix: str, length: int, enter_handle: Callable[[], None]
) -> TextInput:
    """
    Not really a component, it will live on its own thread and render.
    """
    start = f"\x1B[{start_pos[1]+1};{start_pos[0]+1}H"
    write(f"{start}{right_pad(prefix, length)}", True)
    postpref = f"\x1B[{start_pos[1]+1};{start_pos[0]+1+len(prefix)}H"
    pl = len(prefix)

    closure: TextInput

    def closure(ts: terminal_size, z_idx: int) -> tuple[str, Coords]:  # type: ignore[no-redef]
        return (prefix + right_pad(closure.text, length - pl), start_pos)

    closure.text = ""

    def on_key(key: keyboard.Key | keyboard.KeyCode | None) -> None:
        try:
            if isinstance(key, keyboard.KeyCode) and key.char is not None:
                closure.text += key.char
            elif key == keyboard.Key.space:
                closure.text += " "
            elif key == keyboard.Key.backspace:
                closure.text = closure.text[:-1]
            elif key == keyboard.Key.enter:
                enter_handle()
                closure.text = ""
        except Exception as e:
            ...
        write(f"{postpref}{right_pad(closure.text, length-pl)}", True)

    listener = keyboard.Listener(on_press=on_key)
    listener.start()

    return closure


def clear() -> None:
    write("\x1Bc", True)


def done() -> NoReturn:
    while True:
        sleep(600)


def wrap(func: Callable[[], None]) -> Callable[[], None]:
    @wraps(func)
    def wrapper() -> None:
        try:
            clear()
            func()
            done()
        except KeyboardInterrupt:
            write("\x1Bc", True)

    return wrapper


def resize_callback(
    callback: Callable[[], None], delay: float, initial: bool = True
) -> None:
    if initial is True:
        callback()

    def closure() -> NoReturn:
        ts: terminal_size = get_terminal_size()
        while True:
            start = perf_counter()
            new_size = get_terminal_size()
            if new_size != ts:
                ts = new_size
                clear()
                callback()
            delta = perf_counter() - start
            if delta < delay:
                sleep(delay - delta)

    Thread(target=closure, daemon=True).start()


def join_callbacks(callbacks: Iterable[Callable[[], None]]) -> Callable[[], None]:
    def closure() -> None:
        for callback in callbacks:
            callback()

    return closure
