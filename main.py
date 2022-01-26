import os
import platform
from os import getenv
from dotenv import load_dotenv

import disnake
from disnake.ext import tasks, commands
from disnake.ext.commands import Bot
from disnake.ext.commands import Context

from utils.logging import (
    info, debug, error, warning
)

load_dotenv()
intents = disnake.Intents.default()
bot = Bot(command_prefix=getenv("PREFIX"), intents=intents)


def load_commands(command_type: str) -> None:
    """
    Loading commands from cogs
    """

    for file in os.listdir(f"./cogs/{command_type}"):
        if file.endswith(".py"):
            extension = file[:-3]
            try:
                bot.load_extension(f"cogs.{command_type}.{extension}")
                info(f"Loaded extension '{extension}'")
            except Exception as e:
                exception = f"{type(e).__name__}: {e}"
                error(f"Failed to load extension {extension}\n{exception}")


if __name__ == '__main__':
    load_commands("normal")


@bot.event
async def on_ready() -> None:
    """
    The code in this even is executed when the bot is ready
    """

    info(f"Logged in as {bot.user.name}")
    info(f"disnake API version: {disnake.__version__}")
    info(f"Python version: {platform.python_version()}")
    info(f"Running on: {platform.system()} {platform.release()} ({os.name})")


@bot.event
async def on_message(message: disnake.Message) -> None:
    """
    The code in this event is executed every time someone sends a message, with or without the prefix
    :param message: The message that was sent.
    """

    if message.author == bot.user or message.author.bot:
        return
    await bot.process_commands(message)


@bot.event
async def on_command_completion(context: Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed
    :param context: The context of the command that has been executed.
    """

    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    info(
        f"Executed {executed_command} command in {context.guild.name} (ID: {context.message.guild.id}) by {context.message.author} (ID: {context.message.author.id}) "
    )


@bot.event
async def on_command_error(context: Context, error) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error
    :param context: The normal command that failed executing.
    """

    if isinstance(error, commands.CommandOnCooldown):
        minutes, seconds = divmod(error.retry_after, 60)
        hours, minutes = divmod(minutes, 60)
        hours = hours % 24
        embed = disnake.Embed(
            title="Hey, please slow down!",
            description=f"You can use this command again in {f'{round(hours)} hours' if round(hours) > 0 else ''} {f'{round(minutes)} minutes' if round(minutes) > 0 else ''} {f'{round(seconds)} seconds' if round(seconds) > 0 else ''}.",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingPermissions):
        embed = disnake.Embed(
            title="Error!",
            description="You are missing the permission(s) `" + ", ".join(
                error.missing_permissions) + "` to execute this command!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = disnake.Embed(
            title="Error!",
            description=str(error).capitalize(),
            color=0xE02B2B
        )
        await context.send(embed=embed)

bot.run(getenv("TOKEN"))
