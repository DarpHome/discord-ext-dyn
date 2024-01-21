import discord
from discord.ext import commands, dyn

bot = dyn.Bot(command_prefix="!")


# `style`, `label`, `emoji`, are optional, only `custom_id` is required
@bot.button(style=discord.ButtonStyle.primary, label="Add", custom_id="add:{x},{y}")
async def add(ctx: dyn.Context, x: int, y: int) -> None:
    await ctx.respond(f"{x} + {y} = {x + y}", ephemeral=True)


@bot.button(
    style=discord.ButtonStyle.primary, label="Subtract", custom_id="sub:{x},{y}"
)
async def sub(ctx: dyn.Context, x: int, y: int) -> None:
    await ctx.respond(f"{x} - {y} = {x - y}", ephemeral=True)


@bot.button(
    style=discord.ButtonStyle.primary, label="Multiply", custom_id="mul:{x},{y}"
)
async def mul(ctx: dyn.Context, x: int, y: int) -> None:
    await ctx.respond(f"{x} * {y} = {x * y}", ephemeral=True)


@bot.button(style=discord.ButtonStyle.primary, label="Divide", custom_id="div:{x},{y}")
async def div(ctx: dyn.Context, x: int, y: int) -> None:
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
            .add_item(add(x=x, y=y))
            .add_item(sub(x=x, y=y))
            .add_item(mul(x=x, y=y))
            .add_item(div(x=x, y=y))
            .build()
        ),
    )


token = "TOKEN"

bot.run(token)
