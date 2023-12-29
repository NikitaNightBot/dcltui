from .constants import (
    d_horizontal,
    d_vertical,
    d_top_left,
    d_top_right,
    d_bottom_left,
    d_bottom_right,
)
from threading import Thread
from typing import NoReturn, Callable
from .text_utils import write
from time import sleep, perf_counter
from os import terminal_size, get_terminal_size
from .dcl_types import Component, Vec2Tup


def text_line_component(text: str, coords: Vec2Tup) -> Component:
    return Component(
        lambda ts: (coords, (len(text), 1)),
        lambda ts: (text, (0, 0)),
    )


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
        lambda ts: ((0, 0), (ts.columns, ts.lines)),
        closure,
    )


def clear() -> None:
    write("\x1Bc")


def done() -> NoReturn:
    while True:
        sleep(600)


def wrap(func: Callable[[], None]) -> Callable[[], None]:
    def closure() -> None:
        try:
            clear()
            func()
            done()
        except KeyboardInterrupt:
            clear()
        except Exception as exc:
            clear()
            raise exc

    return closure


def resize_thread(
    callback: Callable[[], None] | Callable[[terminal_size], None],
    delay: float,
    initial: bool = True,
    wsize: bool = False,
) -> None:
    def closure() -> NoReturn:
        size = get_terminal_size()

        def so_sorry() -> None:
            callback(size) if wsize else callback()  # type: ignore

        if initial is True:
            so_sorry()
        while True:
            start = perf_counter()
            new_size = get_terminal_size()
            if new_size != size:
                size = new_size
                clear()
                so_sorry()
            delta = perf_counter() - start
            if delta < delay:
                sleep(delay - delta)

    Thread(target=closure, daemon=True).start()
