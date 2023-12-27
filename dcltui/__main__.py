from .common import double_lined_full_renderer
from .renderer import renderer
from .dcl_types import Element, terminal_size
from .text_utils import right_pad
from time import sleep

def main() -> None:
    layout_render = double_lined_full_renderer()

    text = "Hey!"

    def text_component(term_size: terminal_size, z_idx: int) -> Element:
        return (right_pad(text, term_size.columns-2), (1, 1)) # closure :)

    text_render = renderer([text_component])

    layout_render(True)
    text_render(False)

    sleep(1)

    text = "Not hey!"
    text_render(False)

    sleep(1)

    text = "..."
    text_render(False)

    input()


if __name__ == "__main__":
    main()
