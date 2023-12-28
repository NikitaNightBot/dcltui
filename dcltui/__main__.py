from typing import Iterable, Callable
from .common import (
    double_lined_full_component,
    double_lined_box_component,
    text_input_with_handler,
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

    simple_box: Callable[
        [int, int], Component
    ] = lambda x, y: double_lined_box_component(
        lambda ts: ((yst, yst), (box_x_offset + x, boy_y_offset + y))
    )
    text_box: Callable[[str, int, int], Component] = lambda text, i, j: (
        lambda ts: (
            text,
            (box_x_offset + 1 + (xst * i), boy_y_offset + 1 + (yst * j)),
        )
    )

    text_input, input_displ_comp, input_render = text_input_with_handler(
        "Input: ", 20, (50, 2), (50, 3), lambda _: None
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
            text_input,
            input_displ_comp,
        ]  # dont forget to add to your renderer incase you re-render with clear = True to not lose the input stuff
    )

    layout_render = renderer(layout_components)

    resize_callback(join_callbacks([layout_render, input_render]), 1 / 4, True)


if __name__ == "__main__":
    main()
