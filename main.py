# This is the main file for a simple discord bot.
# It is used to create a bot object and run the bot.
# This bot uses the discord.py library.
import asyncio
import os
import discord
from discord import app_commands  # TODO: 20240814: Figure out if this import is needed.
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand
from dotenv import load_dotenv
import quote_unroll
import utilities
import bot  # TODO: 20240814: Figure out if this import is needed.

# To run this bot as-is you need a .env file (the entire filename is four characters: ".env"),
# with the following variables:
# DISCORD_TOKEN=your_bot_token_here
# DEVELOPER_USER_ID=your_user_id_here


load_dotenv(verbose=True)
BOT_TOKEN = str(os.getenv("DISCORD_TOKEN"))
DEVELOPER_USER_ID = int(os.getenv("DEVELOPER_USER_ID"))
# dreamer = discord.Client()
description = """A simple utility bot."""
intents = discord.Intents.default()
intents.members = True
intents.message_content = True


class MyHelpCommand(DefaultHelpCommand):
    # TODO: Move this to utilities.py maybe? (20240723)
    def __init__(self, **options):
        super().__init__(**options)
        self.no_category = options.pop("no_category", "Uncategorized")

    def add_indented_commands(self, commands, *, heading, max_size=None):
        if not commands:
            return

        self.paginator.add_line(heading)
        max_size = max_size or self.get_max_size(commands)

        get_width = discord.utils._string_width
        for command in commands:
            name = command.name
            width = max_size - (get_width(name) - len(name))
            entry = "{0}{1:<{width}} {2}".format(
                self.indent * " ", name, command.short_doc, width=width
            )
            self.paginator.add_line(self.shorten_text(entry))
            self.paginator.add_line("\u200b")  # only changed thing from super >.>


dreamer = commands.Bot(
    command_prefix="!",
    description=description,
    intents=intents,
    allowed_mentions=discord.AllowedMentions().none(),
    help_command=MyHelpCommand(),
)


@dreamer.command(name="gsync", help="Sync commands globally.")
async def gsync(ctx):
    if ctx.author.id != DEVELOPER_USER_ID:
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        print("Syncing commands...")
        synced = await ctx.bot.tree.sync()
        print(synced)
        await ctx.send(f"Synced {len(synced)} commands globally.")
    except Exception as e:
        print(f"Error syncing commands: {e}")
        await ctx.send("An error occurred while syncing commands.")


@dreamer.command(name="lsync", help="Sync commands locally.")
async def lsync(ctx):
    if ctx.author.id != DEVELOPER_USER_ID:
        await ctx.send("You do not have permission to use this command.")
        return

    try:
        print("Syncing commands...")
        synced = await ctx.bot.tree.sync(guild=ctx.guild)
        print(synced)
        await ctx.send(f"Synced {len(synced)} commands locally.")
    except Exception as e:
        print(f"Error syncing commands: {e}")
        await ctx.send("An error occurred while syncing commands.")


@dreamer.event
async def on_ready():
    print("Logged in as")
    print(dreamer.user.name)
    print(dreamer.user.id)
    print("------")


async def main():
    async with dreamer:
        await dreamer.add_cog(quote_unroll.QuoteUnroll(dreamer))
        await dreamer.add_cog(utilities.Utilities(dreamer))
        await dreamer.start(BOT_TOKEN)


asyncio.run(main())
