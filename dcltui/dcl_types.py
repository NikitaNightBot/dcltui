from typing import Callable, TypeAlias, Protocol
from os import terminal_size

Coords: TypeAlias = tuple[int, int]

Element: TypeAlias = tuple[str, Coords]

Component: TypeAlias = Callable[
    [terminal_size, int], Element  # size on render, render (z) idx
]

Renderer: TypeAlias = Callable[[bool], None]

Transform: TypeAlias = Callable[[terminal_size], tuple[tuple[int, int], tuple[int, int]]]

class TextInput(Protocol): # to make lsps happy
    text: str
    @staticmethod
    def __call__(ts: terminal_size, z_idx: int) -> tuple[str, Coords]: ...
