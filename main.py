# This is the main file for a simple discord bot.
# It is used to create a bot object and run the bot.
# This bot uses the discord.py library.
import os
import discord
from discord import Guild
from discord.abc import GuildChannel
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
import validators

load_dotenv(verbose=True)

BOT_TOKEN = str(os.getenv("DISCORD_TOKEN"))
bot = discord.Client()

description = (
    """A simple bot that pastes the contents of the linked message to the channel."""
)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    description=description,
    intents=intents,
    allowed_mentions=discord.AllowedMentions().none(),
)


def url_is_valid(link: str):
    return validators.url(link)


def replace_text_with_quoted_text(message: discord.Message):
    message.content = "> " + message.content
    message.content = message.content.replace("\n", "\n> ")
    return message


def compose_quote(message: discord.Message):
    message = replace_text_with_quoted_text(message)
    quote: str = f'__@{message.author}__ in **#{message.channel}** at <Timestamps included in the "Lucid figures out how the fuck datetimes work" DLC.>:\n'
    quote += message.content
    # if message.edited_at:
    #     quote += f"\n\nEdited at <t:{datetime.timestamp(message.edited_at)}>"
    return quote


# Defines a function that checks if the string passed is a valid discord message URL.
# The function takes a message and a guild ID as arguments and either returns False or a message object.
async def get_message_from_url(link: str):
    # Split the link on slashes.
    split_link = link.split("/")
    # Get server ID, channel ID, and message ID from the link, and store them as integers.
    server_id = int(split_link[4])
    channel_id = int(split_link[5])
    message_id = int(split_link[6])

    # Use the bot to get the guild object.
    guild: Guild = bot.get_guild(server_id)
    # Use the bot to get the channel object.
    channel: GuildChannel = guild.get_channel(channel_id)
    if not isinstance(channel, discord.TextChannel):
        return False
    # Get the message object from the channel.
    message: discord.Message = await channel.fetch_message(message_id)
    try:
        message_content: str = message.content
    except discord.NotFound:
        return False
    except discord.Forbidden:
        return False
    except discord.HTTPException:
        return False
    return message


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
        if url_is_valid(message.content):
            message_from_url = await get_message_from_url(message.clean_content)
            if message_from_url:
                quote = compose_quote(message_from_url)
                if len(message_from_url.attachments) > 1:
                    attachments_to_send = []
                    # For each attacment in message_from_url, convert it to a file then add that file to attachments_to_send.
                    for attachment in message_from_url.attachments:
                        attachments_to_send.append(await attachment.to_file())
                    await message.channel.send(quote, files=attachments_to_send)
                elif len(message_from_url.attachments) == 1:
                    # Convert the only attachment from message_from_url to a file, then add that file to attachment_to_send.
                    attachment_to_send = await message_from_url.attachments[0].to_file()
                    await message.channel.send(quote, file=attachment_to_send)
                else:
                    await message.channel.send(content=quote)


bot.run(BOT_TOKEN)
