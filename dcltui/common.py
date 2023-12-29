from __future__ import annotations
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
from pynput import keyboard
from .text_utils import write, flush, right_pad
from time import sleep, perf_counter
from os import terminal_size, get_terminal_size
from .dcl_types import Component, Vec2Tup, Renderer, Vec2


class TextInput(Component):
    def __init__(
        self: TextInput,
        text: str,
        size: int,
        input_cords: Vec2Tup,
        prefix: str,
        handle: Callable[[str], None],
        start: bool = False,
    ) -> None:
        self.text = text
        self.size = size
        self.input_cords = input_cords
        self.prefix = prefix
        self.handle = handle
        self.renderer = Renderer([self])

        def transform(ts: terminal_size) -> tuple[Vec2Tup, Vec2Tup]:
            return (input_cords, (size, 1))

        def output(ts: terminal_size) -> tuple[str, Vec2Tup]:
            diff = self.size - len(prefix)
            out = prefix + self.text[-diff:]
            return (out, (0, 0))

        super().__init__(transform, output)

        if start is True:
            self.start()

    def on_press(self, key: keyboard.Key | keyboard.KeyCode | None) -> None:
        if isinstance(key, keyboard.KeyCode) and isinstance(key.char, str):
            self.text += key.char
        elif key == keyboard.Key.enter:
            self.handle(self.text)
            self.text = ""
        elif key == keyboard.Key.backspace:
            self.text = self.text[:-1]
        elif key == keyboard.Key.space:
            self.text += " "
        ts = get_terminal_size()
        #write(f"\x1B[{self.input_cords.y+1};{self.input_cords.x+1+len(self.prefix)}H{right_pad(self.text, self.size-len(self.prefix))}\x1B[{ts.lines+1};{ts.columns+1}H", True)
        self.renderer()

    def start(self: TextInput) -> None:
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        self.renderer()
        flush()


def d_box_sized(size: Vec2Tup, coords: Vec2Tup) -> Component:
    size = Vec2.normalize(size)
    fc = size.x - 2
    fl = size.y - 2
    fh = d_horizontal * fc
    mid = "\n".join([f"{d_vertical}{' '*fc}{d_vertical}"] * fl)
    out = f"{d_top_left}{fh}{d_top_right}\n{mid}\n{d_bottom_left}{fh}{d_bottom_right}"
    return Component(lambda ts: (coords, size), lambda ts: (out, (0, 0)))


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


def d_box_input_with_text(
    cords: Vec2Tup,
    size: int,
    text: str,
    input_text: str,
    prefix: str,
    handler: Callable[[str], str],
) -> Renderer:
    cords = Vec2.normalize(cords)
    icords = cords + Vec2(1, 3)
    input_renderer = Renderer(
        [Component(lambda ts: (icords, (size, 1)), lambda ts: (input_text, (0, 0)))]
    )

    def handle_enter(new: str) -> None:
        nonlocal input_text
        input_text = handler(new)
        input_renderer()

    return (
        Renderer(
            [
                d_box_sized((size + 2, 5), cords),
                text_line_component(text, cords + 1),
                TextInput(
                    input_text,
                    size,
                    cords + Vec2(1, 2),
                    prefix,
                    handle_enter,
                    start=True,
                ),
            ]
        )
        | input_renderer
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
