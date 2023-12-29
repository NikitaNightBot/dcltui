from __future__ import annotations
from os import terminal_size, get_terminal_size
from dataclasses import dataclass
from typing import Self, Callable, TypeAlias
from functools import wraps
from textwrap import wrap
from .text_utils import right_pad, write, flush


@dataclass(slots=True, frozen=True)
class Vec2:
    x: int
    y: int

    @staticmethod
    def bind(func: Callable[[int, int], int]) -> Callable[[Vec2, int | Vec2], Vec2]:
        @wraps(func)
        def wrap(self: Vec2, other: int | Vec2) -> Vec2:
            if isinstance(other, int):
                return type(self)(func(self.x, other), func(self.y, other))
            else:
                return type(self)(func(self.x, other.x), func(self.y, other.y))

        return wrap

    __add__ = bind(int.__add__)
    __sub__ = bind(int.__sub__)
    __mul__ = bind(int.__mul__)

    def prod(self: Vec2) -> int:
        return self.x * self.y

    @staticmethod
    def normalize(thing: tuple[int, int] | Vec2) -> Vec2:
        if isinstance(thing, tuple):
            return Vec2(thing[0], thing[1])
        else:
            return thing


@dataclass(slots=True, frozen=True)
class Element:
    text: str
    offset_cords: Vec2  # will be used as relative when in Renderable

    @staticmethod
    def normalize_element(thing: tuple[str, Vec2] | Element) -> Element:
        if isinstance(thing, tuple):
            return Element(thing[0], thing[1])
        else:
            return thing

    @staticmethod
    def normalize_list(thing_s: list[Element] | Element) -> list[Element]:
        if isinstance(thing_s, list):
            return thing_s
        else:
            return [thing_s]

    @staticmethod
    def normalize_what(
        thing: (tuple[str, Vec2Tup] | Element | list[Element])
    ) -> list[Element]:
        if isinstance(thing, (Element, list)):
            elements = Element.normalize_list(thing)
        elif isinstance(thing, tuple):
            cords = thing[1]
            real_cords = Vec2.normalize(cords)
            element = Element.normalize_element((thing[0], real_cords))
            elements = Element.normalize_list(element)
        return elements


Vec2Tup: TypeAlias = Vec2 | tuple[int, int]
Transform: TypeAlias = Callable[
    [terminal_size], tuple[Vec2Tup, Vec2Tup]
]  # start cords, size


Output: TypeAlias = Callable[
    [terminal_size],
    (tuple[str, tuple[int, int] | Vec2] | Element | list[Element]),
]


@dataclass(slots=True, frozen=True)
class Renderable:
    element: Element
    size: Vec2
    start_cords: Vec2

    def render(self: Renderable) -> None:
        text, offset_cords, s_x, s_y = (
            self.element.text,
            self.element.offset_cords,
            self.size.x,
            self.size.y,
        )
        text = text[
            : self.size.prod()
            + text.count("\n")  # this caused so much pain in the ass i cant
        ]
        offset_x, offset_y = offset_cords.x, offset_cords.y
        parts = wrap(text, s_x)
        parts.extend([""] * (s_y - len(parts)))
        for p_idx, part in enumerate(parts):
            padded = right_pad(part, s_x)
            write(
                f"\x1B[{self.start_cords.y+offset_y+1+p_idx};{self.start_cords.x+offset_x+1}H{padded}",
                False,
            )


@dataclass(slots=True)
class Component:
    transform: Transform
    output: Output

    def __or__(self: Self, new_output: Output) -> Self:
        """
        Mutates
        """
        old_output = self.output

        def closure(ts: terminal_size, /) -> list[Element]:
            old = old_output(ts)
            new = new_output(ts)
            return Element.normalize_what(old) + Element.normalize_what(new)

        self.output = closure
        return self

    def __call__(self: Self) -> list[Renderable]:
        ts = get_terminal_size()
        start_cords, size = self.transform(ts)
        start_cords = Vec2.normalize(start_cords)
        size = Vec2.normalize(size)

        return [
            Renderable(element, size, start_cords)
            for element in Element.normalize_what(self.output(ts))
        ]


@dataclass(slots=True, frozen=True)
class Renderer:
    components: list[Component]

    def __or__(self: Renderer, other: Renderer) -> Renderer:
        self.components.extend(other.components)
        return self

    def __call__(self, clear: bool = False) -> None:
        if clear is True:
            write("\x1Bc")
        for component in self.components:
            renderables = component()
            for renderable in renderables:
                renderable.render()
        ts = get_terminal_size()
        write(f"\x1B[{ts.lines+1};{ts.columns+1}H")  # move cursor to end
        flush()
