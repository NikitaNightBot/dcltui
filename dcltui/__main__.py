from typing import Iterable, Callable
from .common import (
    double_lined_full_component,
    double_lined_box_component,
    text_input,
    wrap,
    resize_callback,
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
    layout_components: Iterable[Component] = (
        [double_lined_full_component]
        + [simple_box((xst * x), (yst * y)) for x in range(count) for y in range(count)]
        + [
            (
                lambda ts, z, text=text, i=i, j=j: (
                    text,
                    (box_x_offset + 1 + (xst * i), boy_y_offset + 1 + (yst * j)),
                )
            )  # late binding quick fix
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
            # dont forget to add incase you re-render with clear = True to not lose the input stuff
        ]
    )

    layout_render = renderer(layout_components)

    mut_comp: Component = lambda ts, z: (right_pad(text_in.text, 20), (50, 2))
    mut_render = renderer([mut_comp])

    resize_callback(layout_render, 1 / 24, True)


if __name__ == "__main__":
    main()
