from typing import Callable, Optional, TypeAlias, Protocol
from os import terminal_size

Coords: TypeAlias = tuple[int, int]

Element: TypeAlias = tuple[str, Coords]

Component: TypeAlias = Callable[
    [terminal_size, int], Element  # size on render, render (z) idx
]


class Renderer(Protocol):
    def __call__(self, clear: bool = ..., /) -> None:
        ...


Transform: TypeAlias = Callable[
    [terminal_size], tuple[tuple[int, int], tuple[int, int]]
]


class TextInput(
    Protocol
):  # to make lsps happy, essentially a Component with a text attribute
    text: str

    def __call__(self, ts: terminal_size, z_idx: int, /) -> tuple[str, Coords]:
        ...
