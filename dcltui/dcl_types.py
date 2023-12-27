from typing import Callable, TypeAlias
from os import terminal_size
from sys import stdout

Coords: TypeAlias = tuple[int, int]

Element: TypeAlias = tuple[str, Coords]

Component: TypeAlias = Callable[
    [terminal_size, int], Element  # size on render, render (z) idx
]

Renderer: TypeAlias = Callable[[bool], None]
