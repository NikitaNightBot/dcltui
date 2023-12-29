from .common import wrap, d_box_fullscreen, resize_thread
from .dcl_types import Renderer, Component


@wrap
def main() -> None:
    text = "Hello, World!"
    render = Renderer(
        [
            d_box_fullscreen(),
            Component(lambda ts: (len(text), 1), lambda ts: (text, (1, 1))),
        ]
    )
    resize_thread(render, 1 / 10, True)


if __name__ == "__main__":  # xd
    main()
