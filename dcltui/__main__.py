from .common import wrap, d_box_fullscreen, resize_thread, text_line_component
from .dcl_types import Renderer


@wrap
def main() -> None:
    text = "Hello, World!"

    # fmt: off
    render = Renderer([
        d_box_fullscreen(), 
        text_line_component(text, (1, 1))
    ])
    # fmt: on

    resize_thread(render, 1 / 10, True)


if __name__ == "__main__":  # xd
    main()
