from abc import ABC, abstractmethod
import discord
from discord.ext import commands
from typing import Annotated, Any, Callable, TYPE_CHECKING
import re
import inspect

from .context import Context

from .internal import format_as_regex

from .components import ButtonBuilder, Callback


class Converter:
    @classmethod
    async def resolve(cls, part: str) -> Any:
        raise NotImplemented


class IntConverter(Converter):
    @classmethod
    async def resolve(cls, part: str) -> int:
        return int(part)


Integer = Annotated[int, IntConverter]


class Bot(commands.Bot):
    if TYPE_CHECKING:
        _dyn_buttons: list[ButtonBuilder]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._dyn_buttons = []

    async def add_cog(self, cog: commands.Cog, *args, **kwargs) -> None:
        # TODO: buttons inside cogs
        await super().add_cog(cog, *args, **kwargs)

    async def on_interaction(self, interaction: discord.Interaction) -> None:
        if interaction.data is None:
            return
        match interaction.type:
            case discord.InteractionType.component:
                if interaction.data.get("component_type", 0) == 2:
                    custom_id = interaction.data.get("custom_id", "")
                    for builder in self._dyn_buttons:
                        match = re.match(builder.custom_id, custom_id)
                        if match is None:
                            continue
                        kwargs = {**match.groupdict()}
                        signature = inspect.signature(builder.callback)
                        for param in signature.parameters.values():
                            if param.kind != param.KEYWORD_ONLY:
                                continue
                            # params
                            if param.annotation is param.empty:
                                continue
                            if hasattr(param.annotation, "__metadata__"):
                                converter: Converter = param.annotation.__metadata__[0]
                                kwargs[param.name] = await converter.resolve(
                                    kwargs[param.name]
                                )
                                continue
                            if issubclass(param.annotation, int):
                                kwargs[param.name] = int(kwargs[param.name])
                            elif issubclass(param.annotation, float):
                                kwargs[param.name] = float(kwargs[param.name])
                            elif issubclass(param.annotation, str):
                                pass
                            else:
                                raise TypeError(
                                    f"Unknown annotation: {param.annotation!r}"
                                )

                        await builder.callback(Context(interaction), **kwargs)  # type: ignore

    def add_button(
        self,
        builder: ButtonBuilder,
    ) -> None:
        self._dyn_buttons.append(builder)

    def button(
        self,
        *,
        style: discord.ButtonStyle = discord.ButtonStyle.secondary,
        disabled: bool = False,
        label: str | None = None,
        custom_id: str | None = None,
        template: str,
        emoji: discord.PartialEmoji | discord.Emoji | str | None = None,
    ) -> Callable[[Callback], ButtonBuilder]:
        def decorator(callback: Callback) -> ButtonBuilder:
            builder = ButtonBuilder(
                callback,
                style=style,
                disabled=disabled,
                label=label,
                custom_id=re.compile(
                    format_as_regex(template) if custom_id is None else custom_id
                ),
                template=template,
                emoji=emoji,
            )
            self.add_button(builder)
            return builder

        return decorator
