from typing import Iterable
from .common import (
    double_lined_full_component,
    double_lined_box_component,
    text_input_with_handler,
    wrap,
    resize_callback,
    join_callbacks,
    vec_add,
)
from .renderer import renderer
from .dcl_types import Component


@wrap
def main() -> None:
    text_size: int = 20
    input_cords: tuple[int, int] = (3, 2)
    text_cords: tuple[int, int] = (3, 3)
    

    text_input, input_displ_comp, input_render = text_input_with_handler(
        "Input: ", text_size, input_cords, text_cords, lambda _: None
    )

    input_wrap = double_lined_box_component(
        lambda ts: ((text_size+2, 4), vec_add(input_cords, (-1, -1)))
    )

    layout_components: Iterable[Component] = [
        double_lined_full_component,
        input_wrap,
        text_input,
        input_displ_comp,
    ]  # dont forget to add input related stuff to your renderer to not lose it on re-renders that clear the screen

    layout_render = renderer(layout_components)

    resize_callback(join_callbacks([layout_render, input_render]), 1 / 4, True)


if __name__ == "__main__":
    main()
