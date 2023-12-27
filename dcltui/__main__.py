from .common import double_lined_full_component, double_lined_box_component
from .renderer import renderer
from .dcl_types import Component

def main() -> None:
    simple_box=lambda x,y:double_lined_box_component(lambda ts:((9,9),(3+x,2+y)))
    components: list[Component] = [double_lined_full_component] + [
        simple_box((81*x),(9*y))
        for x in range(3)
        for y in range(3)
    ]
    render = renderer(components)
    render(True)

    input() 


if __name__ == "__main__":
    main()
