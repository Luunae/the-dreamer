# This is the main file for a simple discord bot.
# It is used to create a bot object and run the bot.
# This bot uses the discord.py library.
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import validators

load_dotenv(verbose=True)

BOT_TOKEN = str(os.getenv("DISCORD_TOKEN"))
bot = discord.Client()

description = (
    """A simple bot that pastes the contents of the linked message to the channel."""
)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", description=description, intents=intents)


# Defines a function that checks if the string passed is a valid discord message URL.
# The function takes a message and a guild ID as arguments and returns a boolean.
def is_message_url(message: str, reference_guild_id) -> bool: # reference_guild_id is derived from message.guild of the original message context.
    # If the message is not a valid URL, return False.
    if not validators.url(message):
        return False

    # First split the url on slashes.
    url_split = message.split("/")
    # Then, unpack the guild ID, channel ID, and message IDs, as ints, from url_split.
    guild_id, channel_id, message_id = (
        int(url_split[4]),
        int(url_split[5]),
        int(url_split[6]),
    )
    # Create a guild object from the guild ID.
    guild_object = bot.get_guild(guild_id)
    if reference_guild_id != guild_object:
        return False
    # Create a channel object from the channel ID.
    channel_object = guild_object.get_channel(channel_id)
    # Create a message object from the message ID.
    message_object = channel_object.fetch_message(message_id)
    # Get the message from the message object.
    # Make sure to handle possible exceptions.
    # Possible exceptions include: NotFound, Forbidden, and HTTPException.
    try:
        message_content = message_object.content
    except discord.NotFound:
        return False
    except discord.Forbidden:
        return False
    except discord.HTTPException:
        return False
    return True


@bot.event
async def on_ready():
    print("Logged in as")
    print(bot.user.name)
    print(bot.user.id)
    print("------")


# Start a function that runs on every message.
@bot.event
async def on_message(message):
    # If the message is from a bot, ignore it.
    if message.author.bot:
        return

    # If the message is from a user, and the message starts with the prefix,
    # then run the function.
    if message.content.startswith("http"):
        print(is_message_url(message.content, message.guild))


bot.run(BOT_TOKEN)
