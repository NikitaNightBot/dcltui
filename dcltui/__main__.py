from typing import Iterable, Callable
from .common import (
    double_lined_full_component,
    double_lined_box_component,
    text_input,
    wrap,
    resize_callback,
    join_callbacks,
)
from .renderer import renderer
from .dcl_types import Component
from .text_utils import right_pad


@wrap
def main() -> None:
    xst = 20
    yst = 20
    box_x_offset = 3
    boy_y_offset = 4
    count = 3

    input_pos = (3, 2)

    simple_box: Callable[
        [int, int], Component
    ] = lambda x, y: double_lined_box_component(
        lambda ts: ((yst, yst), (box_x_offset + x, boy_y_offset + y))
    )
    text_box: Callable[[str, int, int], Component] = lambda text, i, j: (
        lambda ts, z: (
            text,
            (box_x_offset + 1 + (xst * i), boy_y_offset + 1 + (yst * j))
        )
    )
    layout_components: Iterable[Component] = (
        [double_lined_full_component]
        + [simple_box((xst * x), (yst * y)) for x in range(count) for y in range(count)]
        + [
            text_box(text, i, j)
            for i, text in enumerate(
                [
                    "\x1B[38;5;196mhey\n... hi\ni\nguess\x1B[0m",
                    "test\nsome\nmulti\nlines",
                    "damn\nthats\ncrazy",
                ]
            )
            for j in range(count)
        ]
        + [
            text_in := text_input(
                input_pos, "Penis: ", 20, lambda: mut_render()
            )  # lazy evaluation -> can use stuff defined later
            # dont forget to add to your render incase you re-render with clear = True to not lose the input stuff
        ]
    )

    layout_render = renderer(layout_components)

    mut_comp: Component = lambda ts, z: (right_pad(text_in.text, 20), (50, 2))
    mut_render = renderer([mut_comp])

    resize_callback(join_callbacks([layout_render, mut_render]), 1 / 4, True)


if __name__ == "__main__":
    main()
