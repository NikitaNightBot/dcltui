from .common import (
    double_lined_full_component,
    double_lined_box_component,
    text_input,
    wrap,
)
from .renderer import renderer
from .dcl_types import Component


@wrap
def main() -> None:
    xst = 20
    yst = 10

    simple_box = lambda x, y: double_lined_box_component(
        lambda ts: ((yst, yst), (3 + x, 4 + y))
    )
    components: list[Component] = (
        [double_lined_full_component]
        + [simple_box((xst * x), (yst * y)) for x in range(3) for y in range(3)]
        + [
            (lambda ts, z, text=text, i=i, j=j: (text, (4 + (xst * i), 5 + (yst * j)))) # late binding quick fix
            for i, text in enumerate(
                [
                    "\x1B[38;5;196mhey\n... hi\ni\nguess\x1B[0m",
                    "test\nsome\nmulti\nlines",
                    "damn\nthats\ncrazy",
                ]
            )
            for j in range(3)
        ]
        + [
            text_in := text_input((3, 2), "Input: ", 20, lambda s: 0)
            # dont forget to add incase you re-render with clear = True to not lose the input stuff
        ]
    )
    render = renderer(components)
    render(True)


if __name__ == "__main__":
    main()
