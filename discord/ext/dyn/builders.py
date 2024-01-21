from discord.ui import View, Item
from .view import DynamicView
from .components import Component
from typing import TYPE_CHECKING


class ViewBuilder:
    if TYPE_CHECKING:
        _components: list[list[Component]]

    def __init__(self) -> None:
        self.clear()

    def clear(self) -> "ViewBuilder":
        self._components = [[], [], [], [], []]
        return self

    def add_component(self, component: Component) -> "ViewBuilder":
        for row in self._components:
            if len(row) < 5:
                row.append(component)
                return self
        raise OverflowError("no available rows")

    def build(self) -> View:
        view = DynamicView(timeout=None)
        for i, row in enumerate(self._components):
            for col in row:
                view.add_item(col.build(i))
        return view
