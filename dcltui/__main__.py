from .common import double_lined_full_renderer, double_lined_full_component, double_lined_box_component
from .renderer import renderer
from .dcl_types import Element, terminal_size
from .text_utils import right_pad
from time import sleep

def main() -> None:
    layout_render = double_lined_full_renderer()

    text = "Hey!"

    def text_component(term_size: terminal_size, z_idx: int) -> Element:
        return (text, (6, 6)) # closure :)

    text_render = renderer([text_component])

    layout_render(True)
    text_render(False)

    sleep(1)

    text = "Not hey!"
    text_render(False)

    sleep(1)

    text = "..."
    text_render(False)

    sleep(1)

    box = double_lined_box_component(lambda term_size:(
        (15, 15//2),
        (5, 5),
    ))
    box_render = renderer([box])
    box_render(False)

    sleep(1)
    full_render = renderer([double_lined_full_component, box, text_component])
    full_render(True)
    
    input()


if __name__ == "__main__":
    main()
