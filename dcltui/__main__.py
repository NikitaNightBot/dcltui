from .common import (
    double_lined_full_component,
    double_lined_box_component,
    text_input,
    wrap,
    right_pad,
)
from .renderer import renderer
from .dcl_types import Component


@wrap
def main() -> None:
    xst = 20
    yst = 10
    box_x_offset = 3
    boy_y_offset = 4
    count = 3

    input_pos = (3, 2)

    simple_box = lambda x, y: double_lined_box_component(
        lambda ts: ((yst, yst), (box_x_offset + x, boy_y_offset + y))
    )
    layout_components: list[Component] = (
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
                input_pos, "Input: ", 20, lambda s: mut_render()
            )  # lazy evaluation -> can use stuff defined later
            # dont forget to add incase you re-render with clear = True to not lose the input stuff
        ]
    )

    layout_render = renderer(layout_components)

    mut_comp = lambda ts, z: (right_pad(text_in.text, 20), (50, 2))
    mut_render = renderer([mut_comp])

    layout_render(True)


if __name__ == "__main__":
    main()
