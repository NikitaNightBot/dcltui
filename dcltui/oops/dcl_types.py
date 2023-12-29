from __future__ import annotations
from os import terminal_size
from dataclasses import dataclass
from typing import Self, Callable, TypeAlias, Type
from functools import wraps


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


Transform: TypeAlias = Callable[[terminal_size], Vec2]
Output: TypeAlias = (
    Callable[[terminal_size], Element] | Callable[[terminal_size], list[Element]]
)


@dataclass(slots=True)
class Component:
    transform: Transform
    output: Output

    def __or__(self: Self, new_output: Output) -> Self:
        def closure(ts: terminal_size, /) -> list[Element]:
            old = self.output(ts)
            new = new_output(ts)
            return Element.normalize_list(old) + Element.normalize_list(new)

        return type(self)(
            self.transform,
            closure,
        )
