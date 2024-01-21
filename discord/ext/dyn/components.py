from abc import ABC, abstractmethod

import discord
from discord import ui
from typing import TYPE_CHECKING, Callable
import re


class Component(ABC):
    @abstractmethod
    def build(self, row: int) -> ui.Item:
        ...


# class Callback(Protocol):
#    async def __call__(self, ctx: Context, kwargs: ...) -> None:
#        ...

Callback = Callable[..., None]


class ButtonComponent(Component):
    if TYPE_CHECKING:
        style: discord.ButtonStyle
        label: str | None
        disabled: bool
        custom_id: str
        emoji: discord.PartialEmoji | discord.Emoji | str | None

    def __init__(
        self,
        *,
        style: discord.ButtonStyle,
        disabled: bool = False,
        custom_id: str,
        label: str | None = None,
        emoji: discord.PartialEmoji | discord.Emoji | str | None = None
    ) -> None:
        self.style = style
        self.label = label
        self.disabled = disabled
        self.custom_id = custom_id
        self.emoji = emoji

    def build(self, row: int) -> ui.Item:
        return ui.Button(
            style=self.style,
            custom_id=self.custom_id,
            disabled=self.disabled,
            label=self.label,
            emoji=self.emoji,
            row=row,
        )


class Builder(ABC):
    pass


class ButtonBuilder(Builder):
    if TYPE_CHECKING:
        callback: Callback
        style: discord.ButtonStyle
        label: str | None
        disabled: bool
        custom_id: re.Pattern
        template: str
        emoji: discord.PartialEmoji | discord.Emoji | str | None

    def __init__(
        self,
        callback: Callback,
        *,
        style: discord.ButtonStyle,
        disabled: bool = False,
        custom_id: re.Pattern,
        template: str,
        label: str | None = None,
        emoji: discord.PartialEmoji | discord.Emoji | str | None = None
    ) -> None:
        self.callback = callback
        self.style = style
        self.label = label
        self.disabled = disabled
        self.custom_id = custom_id
        self.template = template
        self.emoji = emoji

    def __call__(self, **kwargs) -> ButtonComponent:
        return ButtonComponent(
            style=self.style,
            disabled=self.disabled,
            custom_id=self.template.format(**kwargs),
            label=self.label,
            emoji=self.emoji,
        )
