from __future__ import annotations

from typing import Callable, TypeAlias
from os import get_terminal_size, terminal_size
from sys import stdout

def write(
    text: str, 
    flush: bool = False, 
    w=stdout.write, f=stdout.flush # local names faster lookup
) -> None:
    w(text)
    if flush:
        f()

Component: TypeAlias = Callable[
    [terminal_size, int], # size on render, render (z) idx
    tuple[
        str, # want to feature some sort of custom template strings later
        tuple[int, int] # start coordinates
    ] 
]

def renderer(
    components: list[Component], 
) -> Callable[[bool], None]:
    def closure(clear: bool = True) -> None:
        term_size: terminal_size = get_terminal_size()

        if clear is True:
            fill = ' '*term_size.columns
            write('\n'.join([fill]*term_size.lines), True)

        for z_idx, component in enumerate(components):
            text, (start_x, start_y) = component(term_size, z_idx)
            for line_idx, line in enumerate(text.splitlines()):
                write(f"\x1B[{line_idx+start_y+1};{start_x+1}H{line}", flush=True)
                
    return closure

def main() -> None:
    def box(term_size: terminal_size, z_idx: int) -> tuple[str, tuple[int, int]]:
        
        return ("""\
.---.
|   |
|   |
.---.""", (0, 0))
    components = [box]
    render = renderer(components)
    render()
    input()

if __name__ == "__main__":
    main()