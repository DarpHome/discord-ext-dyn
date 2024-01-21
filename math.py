import discord
from discord.ext import commands, dyn
import os

bot = dyn.Bot(
    command_prefix="!", intents=discord.Intents(messages=True, message_content=True)
)


# `style`, `label`, `emoji`, are optional, only `custom_id` is required
@bot.button(
    style=discord.ButtonStyle.primary,
    label="Add",
    template="add:{x},{y}",
)
async def add(ctx: dyn.Context, *, x: int, y: int) -> None:
    await ctx.respond(f"{x} + {y} = {x + y}", ephemeral=True)


@bot.button(
    style=discord.ButtonStyle.primary,
    label="Subtract",
    template="sub:{x},{y}",
)
async def sub(ctx: dyn.Context, *, x: int, y: int) -> None:
    await ctx.respond(f"{x} - {y} = {x - y}", ephemeral=True)


@bot.button(
    style=discord.ButtonStyle.primary,
    label="Multiply",
    template="mul:{x},{y}",
)
async def mul(ctx: dyn.Context, *, x: int, y: int) -> None:
    await ctx.respond(f"{x} * {y} = {x * y}", ephemeral=True)


@bot.button(
    style=discord.ButtonStyle.primary,
    label="Divide",
    template="div:{x},{y}",
)
async def div(ctx: dyn.Context, *, x: int, y: int) -> None:
    if y == 0:
        await ctx.respond(f"Cannot divide by zero", ephemeral=True)
        return
    await ctx.respond(f"{x} / {y} = {x / y}", ephemeral=True)


@bot.command()
async def math(ctx: commands.Context, x: int, y: int) -> None:
    await ctx.send(
        "Math is fun",
        view=(
            dyn.ViewBuilder()
            .add_component(add(x=x, y=y))
            .add_component(sub(x=x, y=y))
            .add_component(mul(x=x, y=y))
            .add_component(div(x=x, y=y))
            .build()
        ),
    )


token = os.environ["TOKEN"]

bot.run(token)
