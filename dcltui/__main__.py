from .common import double_lined_full_renderer
from .renderer import renderer
from .dcl_types import Element, terminal_size


def main() -> None:
    layout_render = double_lined_full_renderer()

    text = "Hey!"

    def text_component(term_size: terminal_size, z_idx: int) -> Element:
        return (text, (1, 1))

    text_render = renderer([text_component])

    layout_render(True)
    text_render(False)

    input()


if __name__ == "__main__":
    main()
