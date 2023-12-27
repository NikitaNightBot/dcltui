from .common import double_lined_full_layout
from .renderer import renderer

def main() -> None:
    render = renderer([
        double_lined_full_layout
    ])

    render()
    input()

if __name__ == "__main__":
    main()