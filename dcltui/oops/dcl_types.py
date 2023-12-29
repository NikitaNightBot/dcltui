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

    @staticmethod
    def normalize(thing: tuple[int, int] | Vec2) -> Vec2:
        if isinstance(thing, tuple):
            return Vec2(thing[0], thing[1])
        else:
            return thing


@dataclass(slots=True, frozen=True)
class Element:
    text: str
    cords: Vec2

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
        thing: (
            tuple[str, tuple[int, int]] | tuple[str, Vec2] | Element | list[Element]
        )
    ) -> list[Element]:
        if isinstance(thing, (Element, list)):
            elements = Element.normalize_list(thing)
        elif isinstance(thing, tuple):
            cords = thing[1]
            real_cords = Vec2.normalize(cords)
            element = Element.normalize_element((thing[0], real_cords))
            elements = Element.normalize_list(element)
        return elements


Transform: TypeAlias = (
    Callable[[terminal_size], Vec2] | Callable[[terminal_size], tuple[int, int]]
)
Output: TypeAlias = (
    Callable[[terminal_size], tuple[str, tuple[int, int]]]
    | Callable[[terminal_size], tuple[str, Vec2]]
    | Callable[[terminal_size], Element]
    | Callable[[terminal_size], list[Element]]
)


@dataclass(slots=True, frozen=True)
class Renderable:
    element: Element
    size: Vec2

    def render(self: Renderable) -> None:
        text, cords, s_x, s_y = self.element.text, self.element.cords, self.size.x, self.size.y
        st_x, st_y = cords.x, cords.y
        parts = wrap(text, s_x)
        parts.extend([""]*(s_y-len(parts)))
        for p_idx, part in enumerate(parts):
            padded = right_pad(part, s_x)
            write(f"\x1B[{st_y+1+p_idx};{st_x+1}H{padded}", False)


@dataclass(slots=True)
class Component:
    transform: Transform
    output: Output

    def __or__(self: Self, new_output: Output) -> Self:
        def closure(ts: terminal_size, /) -> list[Element]:
            old = self.output(ts)
            new = new_output(ts)
            return Element.normalize_what(old) + Element.normalize_what(new)

        return type(self)(
            self.transform,
            closure,
        )

    def __call__(self: Self) -> list[Renderable]:
        ts = get_terminal_size()
        size = Vec2.normalize(self.transform(ts))
        return [
            Renderable(element, size)
            for element in Element.normalize_what(self.output(ts))
        ]


@dataclass(slots=True, frozen=True)
class Renderer:
    components: list[Component]

    def __or__(self: Renderer, other: Renderer) -> Renderer:
        return Renderer(self.components + other.components)

    def __call__(self, clear: bool = False) -> None:
        if clear is True:
            write("\x1Bc")
        for component in self.components:
            renderables = component()
            for renderable in renderables:
                renderable.render()
        flush()
