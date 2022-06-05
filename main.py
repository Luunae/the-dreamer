# This is the main file for a simple discord bot.
# It is used to create a bot object and run the bot.
# This bot uses the discord.py library.
import os
import discord
from discord.ext import commands
from discord.ext.commands import DefaultHelpCommand
from dotenv import load_dotenv
import quote_unroll
import utilities
import bot

load_dotenv(verbose=True)
BOT_TOKEN = str(os.getenv("DISCORD_TOKEN"))
# dreamer = discord.Client()
description = """A simple utility bot."""
intents = discord.Intents.default()
intents.members = True


class MyHelpCommand(DefaultHelpCommand):
    def __init__(self, **options):
        super().__init__(**options)
        self.no_category = options.pop('no_category', 'Uncategorized')

    def add_indented_commands(self, commands, *, heading, max_size=None):
        if not commands:
            return

        self.paginator.add_line(heading)
        max_size = max_size or self.get_max_size(commands)

        get_width = discord.utils._string_width
        for command in commands:
            name = command.name
            width = max_size - (get_width(name) - len(name))
            entry = '{0}{1:<{width}} {2}'.format(self.indent * ' ', name, command.short_doc, width=width)
            self.paginator.add_line(self.shorten_text(entry))
            self.paginator.add_line('\u200b')  # only changed thing from super >.>


dreamer = commands.Bot(
    command_prefix="!",
    description=description,
    intents=intents,
    allowed_mentions=discord.AllowedMentions().none(),
    help_command=MyHelpCommand()
)


@dreamer.event
async def on_ready():
    print("Logged in as")
    print(dreamer.user.name)
    print(dreamer.user.id)
    print("------")


dreamer.add_cog(quote_unroll.QuoteUnroll(dreamer))
dreamer.add_cog(utilities.Utilities(dreamer))
dreamer.run(BOT_TOKEN)
bot.instance = dreamer
