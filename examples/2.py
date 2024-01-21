import discord
from discord.ext import commands, dyn

bot = dyn.Bot(command_prefix="!")


@bot.modal("introduction", title="Introduction")
async def introduction(
    ctx: dyn.ModalContext, name: str = dyn.TextInput(style=discord.TextStyle.short)
) -> None:
    await ctx.respond(f"Hello, {name}!", ephemeral=True)


@bot.tree.command()
async def math(interaction: discord.Interaction) -> None:
    await interaction.response.send_modal(introduction())


token = "TOKEN"

bot.run(token)
