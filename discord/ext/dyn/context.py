import discord
from typing import TYPE_CHECKING


class Context:
    if TYPE_CHECKING:
        interaction: discord.Interaction

    def __init__(self, interaction: discord.Interaction) -> None:
        self.interaction = interaction

    async def respond(self, *args, **kwargs) -> None:
        return await self.interaction.response.send_message(*args, **kwargs)
