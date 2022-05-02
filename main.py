# This is the main file for a simple discord bot.
# It is used to create a bot object and run the bot.
# This bot uses the discord.py library.
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import quote_unroll
import teleport
import bot

load_dotenv(verbose=True)

BOT_TOKEN = str(os.getenv("DISCORD_TOKEN"))
# dreamer = discord.Client()

description = """A simple utility bot."""

intents = discord.Intents.default()
intents.members = True

dreamer = commands.Bot(
    command_prefix="!",
    description=description,
    intents=intents,
    allowed_mentions=discord.AllowedMentions().none(),
)


@dreamer.event
async def on_ready():
    print("Logged in as")
    print(dreamer.user.name)
    print(dreamer.user.id)
    print("------")


dreamer.add_cog(quote_unroll.QuoteUnroll(dreamer))
dreamer.add_cog(teleport.Teleport(dreamer))
dreamer.run(BOT_TOKEN)
bot.instance = dreamer
