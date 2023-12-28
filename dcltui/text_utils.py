from sys import stdout
from typing import Callable


def write(
    text: str,
    flush: bool = False,
    w: Callable[[str], int | None] = stdout.write,
    f: Callable[[], None] = stdout.flush,  # local names faster lookup
) -> None:
    w(text)
    if flush:
        f()


def left_pad(text: str, size: int) -> str:
    return ((" " * (size - len(text))) + text)[-size:]


def right_pad(text: str, size: int) -> str:
    return (text + (" " * (size - len(text))))[-size:]
