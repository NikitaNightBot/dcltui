from .common import (
    wrap,
    d_box_fullscreen,
    resize_thread,
    d_box_input_with_text,
)
from .dcl_types import Renderer


@wrap
def main() -> None:
    text = "Hello, World!"
    size = len(text)

    input_renderer = d_box_input_with_text((1, 1), size, text, "", "> ", lambda s: s)

    render = Renderer([d_box_fullscreen()]) | input_renderer

    resize_thread(render, 1 / 10, True)


if __name__ == "__main__":  # xd
    main()
